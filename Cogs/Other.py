import configparser
from discord.ext import commands

# Set up config reader
config = configparser.ConfigParser()
config.read('config.ini')


class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bot commands
    @commands.command(brief='',
                      description='')
    async def test(self, ctx):
        await ctx.send('Hello world')


# Add cog to discord bot
async def setup(bot):
    await bot.add_cog(Other(bot))
