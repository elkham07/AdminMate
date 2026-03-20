from flask import Flask, request, jsonify
import discord
import os
import asyncio

app = Flask(__name__)

bot_instance = None

def set_bot(bot):
    global bot_instance
    bot_instance = bot

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('action')
    membership = data.get('data', {})
    discord_id = membership.get('discord', {}).get('id')

    if not discord_id or not bot_instance:
        return jsonify({'status': 'error'}), 200

    asyncio.run_coroutine_threadsafe(
        handle_role(event, discord_id),
        bot_instance.loop
    )
    return jsonify({'status': 'ok'}), 200

async def handle_role(event, discord_id):
    guild = bot_instance.guilds[0] if bot_instance.guilds else None
    if not guild:
        return

    member = guild.get_member(int(discord_id))
    role = discord.utils.get(guild.roles, name='Premium')

    if not role:
        role = await guild.create_role(name='Premium')

    if event == 'membership.went_valid' and member:
        await member.add_roles(role)
    elif event == 'membership.went_invalid' and member:
        await member.remove_roles(role)

def run_flask():
    app.run(host='0.0.0.0', port=5005)