import configparser
import discord
import os
from discord.ext import commands

creds = configparser.ConfigParser()
config = configparser.ConfigParser()
creds.read('credentials.ini')
config.read('config.ini')

token = creds['DISCORD']['token']
prefix = config['DISCORD']['prefix']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=prefix, description='Dottie Rulez', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')

bot.run(token)
