import configparser
import discord
import Utils
from discord.ext import commands

# Set up config reader
config = configparser.ConfigParser()
config.read('config.ini')

admin_role_id = int(config['ROLES']['admin'])
complaint_channel_id = int(config['CHANNELS']['complaint_channel'])
default_embed_color = config['EMBED']['default_color']


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bot commands

    @commands.command(brief='',
                      description='',
                      aliases=['complaint', 'report'])
    @commands.dm_only()
    async def complain(self, ctx):
        complaint_channel = self.bot.get_channel(complaint_channel_id)
        await Utils.submit_complaint(ctx, complaint_channel)

    @commands.command(brief='Bot does a quit',
                      description='This kills the bot.')
    @commands.has_role(admin_role_id)
    async def exit(self, ctx):
        await ctx.send('Bye.')
        await self.bot.close()


# Add cog to discord bot
async def setup(bot):
    await bot.add_cog(Admin(bot))
