import configparser
import discord
import Utils
from discord.ext import commands

# Set up config reader
config = configparser.ConfigParser()
config.read('config.ini')

admin_role_id = int(config['ROLES']['admin'])
complaint_channel_id = int(config['CHANNELS']['complaint_channel'])


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bot commands

    @commands.command(brief='',
                      description='',
                      aliases=['complaint', 'report'])
    @commands.dm_only()
    async def complain(self, ctx, *, complaint):
        await ctx.send(Utils.complaint_warning)
        complaint_channel = self.bot.get_channel(complaint_channel_id)
        await complaint_channel.send(f"**The following anonymous complaint has been submitted:**\r\n> {complaint}")

        view = discord.ui.View()

        async def respond_dialog(interaction):
            response_modal = Utils.ResponseDialog()
            await interaction.response.send_modal(response_modal)
            await response_modal.wait()
            return

        async def respond_to_sender(interaction):
            await interaction.response.defer()
            await ctx.send(f"**Mods have sent the following response:**\r\n> {interaction.message.content}")
            await interaction.message.edit(content=f'**The following response has been sent:**\n\n> {interaction.message.content}', view=None, embed=None)

        async def reveal_sender(interaction):
            # TODO
            # ping mods and say that <user> has requested the following name be revealed and requires a :thumbsup: react from all mods pls react
            # add thumbs up by default
            # wait for add_reaction and check if # of reacts > 5
            # if so, await complaint channel.send ctx.author.name
            return

        respond_button = discord.ui.Button(label="Edit Response", style=discord.ButtonStyle.gray)
        submit_button = discord.ui.Button(label="Submit Response", style=discord.ButtonStyle.blurple)
        reveal_button = discord.ui.Button(label="Reveal Sender", style=discord.ButtonStyle.danger)

        respond_button.callback = respond_dialog
        submit_button.callback = respond_to_sender
        reveal_button.callback = reveal_sender

        view.add_item(reveal_button)
        view.add_item(respond_button)
        view.add_item(submit_button)

        await complaint_channel.send(view=view)

    @commands.command(brief='Bot does a quit',
                      description='This kills the bot.')
    @commands.has_role(admin_role_id)
    async def exit(self, ctx):
        await ctx.send('Bye.')
        await self.bot.close()


# Add cog to discord bot
async def setup(bot):
    await bot.add_cog(Admin(bot))
