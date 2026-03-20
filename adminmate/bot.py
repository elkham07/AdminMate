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
            f"🎉 {message.author.mention} reached the level **{new_level}**!"
        )
 
    await bot.process_commands(message)
 
        
        
    
        

