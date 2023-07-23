import configparser
from discord.ext import commands


class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('config.ini')

    @commands.command(brief='',
                      description='')
    async def test(self, ctx):
        await ctx.send('Hello world')


async def setup(bot):
    await bot.add_cog(Other(bot))
