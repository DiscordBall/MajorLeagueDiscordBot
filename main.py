import configparser
import discord
import logging
import os
from discord.ext import commands

# Set up config reader
creds = configparser.ConfigParser()
config = configparser.ConfigParser()
creds.read('credentials.ini')
config.read('config.ini')

# Get values from config file
token = creds['DISCORD']['token']
prefix = config['DISCORD']['prefix']
log_channel = int(config['CHANNELS']['log_channel'])

bot = commands.Bot(command_prefix=prefix, description='Disco Rulez', case_insensitive=True, intents=discord.Intents.all())


# Initial setup once bot is running
@bot.event
async def on_ready():
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')
    print('ready')


# Catch common bot errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission to use that command.")
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing a required argument. Please use `.help {ctx.command}` for more information.")
        return
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be done in private message.")
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Please wait {int(error.retry_after)} seconds.")
        return
    else:
        await bot.get_channel(log_channel).send(error)


bot.run(token, log_level=logging.WARNING)
