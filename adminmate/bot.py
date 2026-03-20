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

