import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import asyncio
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
 
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
 
bot = commands.Bot(command_prefix='!', intents=intents)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}
 
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)



xp_data = load_data('xp.json')
 
def get_level(xp):
    return int(xp ** 0.5) // 10
 
@bot.event
async def on_message(message):
    if message.author.bot:
        return
 
   
    user_id = str(message.author.id)
    member = message.guild.get_member(message.author.id)
    days_on_server = (datetime.utcnow() - member.joined_at.replace(tzinfo=None)).days
 
    if days_on_server < 7:
        bad_words = ['http://', 'https://', 'discord.gg']
        if any(word in message.content.lower() for word in bad_words):
            await message.delete()
            await message.channel.send(
                f"⚠️ {message.author.mention}, New members cannot be sent links for the first 7 days.",
                delete_after=5
            )
            return
        
         
        if user_id not in xp_data:
            xp_data[user_id] = {'xp': 0, 'level': 0}
 
    old_level = xp_data[user_id]['level']
    xp_data[user_id]['xp'] += 10
    new_level = get_level(xp_data[user_id]['xp'])
    xp_data[user_id]['level'] = new_level
    save_data('xp.json', xp_data)
 
   
    if new_level > old_level:
        await message.channel.send(
            f" {message.author.mention} reached the level **{new_level}**!"
        )
 
    await bot.process_commands(message)
 
        
        
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='общий')
    if channel:
        embed = discord.Embed(
            title=f"What's up, {member.name}!",
            description=f"You have become  **{member.guild.member_count}-м** member of the server!\nCheck the rules and introduce yourself in the chat.",
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)
    
        

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.name} has been banned. Reason: {reason}")
 
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.name} has been kicked. Reason: {reason}")
 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Deleted {amount} messages.", delete_after=3)
 
@bot.command()
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    warns = load_data('warns.json')
    user_id = str(member.id)
    if user_id not in warns:
        warns[user_id] = []
    warns[user_id].append({
        'reason': reason,
        'date': str(datetime.utcnow()),
        'by': str(ctx.author)
    })
    save_data('warns.json', warns)
    count = len(warns[user_id])
    await ctx.send(f"⚠️ {member.mention} received a warning ({count}/3). Reason: {reason}")
 
    if count >= 3:
        await member.kick(reason="3 warnings")
        await ctx.send(f"👢 {member.name} was kicked for receiving 3 warnings.")
 

@bot.command()
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)
    if user_id not in xp_data:
        await ctx.send(f"{member.name} has not earned any XP yet.")
        return
    xp = xp_data[user_id]['xp']
    lvl = xp_data[user_id]['level']
    embed = discord.Embed(
        title=f"Level — {member.name}",
        color=0x5865F2
    )
    embed.add_field(name="Level", value=str(lvl))
    embed.add_field(name="XP", value=str(xp))
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def digest(ctx):
    guild_id = str(ctx.guild.id)
    messages = digest_messages.get(guild_id, [])
 
    if not messages:
        await ctx.send("No data available for the digest.")
        return
 
    total = len(messages)
    channels = {}
    for msg in messages:
        ch = msg['channel']
        channels[ch] = channels.get(ch, 0) + 1
 
    top_channel = max(channels, key=channels.get) if channels else "no data"
 
    embed = discord.Embed(
        title="Weekly Server Digest",
        description="Activity summary for the recent period",
        color=0x5865F2,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Total messages", value=str(total), inline=True)
    embed.add_field(name="Most active channel", value=f"#{top_channel}", inline=True)
    embed.add_field(name="Server members", value=str(ctx.guild.member_count), inline=True)
    embed.set_footer(text="AdminMate • Digest")
    await ctx.send(embed=embed)
 
 
@bot.command()
async def ticket(ctx, *, problem="No problem specified"):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
    }
    channel = await guild.create_text_channel(
        f'ticket-{ctx.author.name}',
        overwrites=overwrites
    )
    embed = discord.Embed(
        title="New Ticket",
        description=f"**User:** {ctx.author.mention}\n**Problem:** {problem}",
        color=0x5865F2
    )
    embed.set_footer(text="Type !close to close the ticket")
    await channel.send(embed=embed)
    await ctx.send(f"Ticket created: {channel.mention}")
 
@bot.command()
async def close(ctx):
    if 'ticket' in ctx.channel.name:
        await ctx.send("Ticket closing in 5 seconds...")
        await asyncio.sleep(5)
        await ctx.channel.delete()
 
@bot.event
async def on_ready():
    print(f'Bot {bot.user} is online and ready!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="over the server"
    ))
 
bot.run(TOKEN)
 