import configparser
from discord.ext import commands

# Set up config reader
config = configparser.ConfigParser()
config.read('config.ini')
admin = int(config['ROLES']['admin'])


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bot commands
    @commands.command(brief='Bot does a quit',
                      description='This kills the bot.')
    @commands.has_role(admin)
    async def exit(self, ctx):
        await ctx.send('Bye.')
        await self.bot.close()


# Add cog to discord bot
async def setup(bot):
    await bot.add_cog(Admin(bot))
