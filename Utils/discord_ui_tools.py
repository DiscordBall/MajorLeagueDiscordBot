import configparser
import discord

import Utils

config = configparser.ConfigParser()
config.read('config.ini')


# Classes
class ComplaintDialog(discord.ui.Modal, title="Submit a Complaint"):
    complaint_input = discord.ui.TextInput(label='Complaint', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()


class ResponseDialog(discord.ui.Modal, title="Respond to a complaint"):
    response_input = discord.ui.TextInput(label='Response', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()


# Functions
def cancel_button():
    async def cancel_function(interaction):
        await interaction.response.edit_message(content='Request cancelled.', view=None, embed=None)
        return

    cancel = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.red)
    cancel.callback = cancel_function
    return cancel


def submit_button(submit_channel):
    async def submit_function(interaction):
        await interaction.response.defer()
        await submit_channel.send(interaction.message.content)
        return

    submit = discord.ui.Button(label="Submit", style=discord.ButtonStyle.green)
    submit.callback = submit_function
    return submit


def default_embed(title: str, description: str = None, color: str = None):
    if color:
        color = discord.Color(value=int(color, 16))
    else:
        color = discord.Color(value=int(config['EMBED']['default_color'], 16))
    if description:
        embed = discord.Embed(title=title, description=description, color=color)
    else:
        embed = discord.Embed(title=title, color=color)
    embed.set_footer(text=config['EMBED']['default_footer'], icon_url=config['EMBED']['default_thumbnail'])
    return embed


async def respond_to_complaint(ctx, complaint_channel, complaint: str, anonymous: bool = True):
    if anonymous:
        title = "Anonymous Complaint"
    else:
        title = f"Complaint Submitted by {ctx.author}"
    embed = default_embed(title=title)
    embed.add_field(name="Complaint", value=complaint, inline=False)
    embed.add_field(name='Response', value='-', inline=False)

    async def respond_dialog(interaction):
        response_modal = ResponseDialog()
        await interaction.response.send_modal(response_modal)
        await response_modal.wait()
        embed.set_field_at(1, name='Response', value=response_modal.response_input.value, inline=False)
        await interaction.message.edit(embed=embed)
        return

    async def respond_to_sender(interaction):
        await interaction.response.defer()
        await ctx.send(embed=embed)
        await interaction.message.edit(
            content=f'Response sent.', view=None)

    async def reveal_sender(interaction):
        await interaction.response.defer()
        react_limit = int(config['MOD']['reveal_username_reacts'])
        admin_role = config['ROLES']['admin']
        react_msg = await interaction.followup.send(f"<@&{admin_role}> {interaction.user.mention} has requested the above username be revealed. {react_limit} 👍 reacts are required to reveal this information.")
        await react_msg.add_reaction('👍')
        await react_msg.add_reaction('👎')

        def check(reaction, user):
            if reaction.message == react_msg and reaction.emoji == '👍' and reaction.count > react_limit:
                return True

        await interaction.client.wait_for('reaction_add', timeout=None, check=check)
        await interaction.followup.send(f'Complaint was submitted by {ctx.author.mention}')
        await ctx.send(f"{ctx.author.mention} your username has been revealed for sending the above anonymous complaint.")

    edit_response_button = discord.ui.Button(label="Edit Response", style=discord.ButtonStyle.gray)
    submit_response_button = discord.ui.Button(label="Submit Response", style=discord.ButtonStyle.blurple)
    reveal_button = discord.ui.Button(label="Reveal Sender", style=discord.ButtonStyle.danger)

    edit_response_button.callback = respond_dialog
    submit_response_button.callback = respond_to_sender
    reveal_button.callback = reveal_sender

    response_view = discord.ui.View()
    if anonymous:
        response_view.add_item(reveal_button)
    response_view.add_item(edit_response_button)
    response_view.add_item(submit_response_button)

    await complaint_channel.send(embed=embed, view=response_view)


async def submit_complaint(ctx, complaint_channel):
    embed = Utils.default_embed(title="Submit a Complaint", description=Utils.complaint_warning)

    embed.add_field(name="Complaint", value="-")

    edit_complaint_button = discord.ui.Button(label="Add/Edit Complaint", style=discord.ButtonStyle.grey)
    submit_as_me_button = discord.ui.Button(label=f"Submit as {ctx.author}", style=discord.ButtonStyle.blurple, row=2)
    submit_anonymous_button = discord.ui.Button(label=f"Submit Anonymously", style=discord.ButtonStyle.blurple, row=2)

    async def edit_complaint(interaction):
        response_modal = ComplaintDialog()
        await interaction.response.send_modal(response_modal)
        await response_modal.wait()
        embed.set_field_at(0, name='Complaint', value=response_modal.complaint_input.value, inline=False)
        await interaction.message.edit(embed=embed)
        return

    async def submit_as_anonymous(interaction):
        await interaction.response.defer()
        await interaction.message.edit(view=None)
        await interaction.followup.send("The above complaint has been submitted.")
        await respond_to_complaint(ctx, complaint_channel, embed.fields[0].value, True)
        return

    async def submit_as_me(interaction):
        await interaction.response.defer()
        await interaction.message.edit(view=None)
        await interaction.followup.send("The above complaint has been submitted.")
        await respond_to_complaint(ctx, complaint_channel, embed.fields[0].value, False)
        return

    edit_complaint_button.callback = edit_complaint
    submit_anonymous_button.callback = submit_as_anonymous
    submit_as_me_button.callback = submit_as_me

    complaint_view = discord.ui.View()

    complaint_view.add_item(edit_complaint_button)
    complaint_view.add_item(Utils.cancel_button())
    complaint_view.add_item(submit_as_me_button)
    complaint_view.add_item(submit_anonymous_button)

    await ctx.send(embed=embed, view=complaint_view)
