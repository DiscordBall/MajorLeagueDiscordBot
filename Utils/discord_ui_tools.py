import discord


# Classes
class ResponseDialog(discord.ui.Modal, title="Respond to a complaint"):
    response_input = discord.ui.TextInput(label='Response', style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.edit(content=self.response_input)


# Functions
def add_submit_button(view: discord.ui.View, submit_channel):
    async def submit_function(interaction):
        await interaction.response.defer()
        await submit_channel.send(interaction.message.content)
        return

    submit_button = discord.ui.Button(label="Submit", style=discord.ButtonStyle.green)
    submit_button.callback = submit_function
    view.add_item(submit_button)


def add_cancel_button(view: discord.ui.View):
    async def cancel_function(interaction):
        await interaction.response.edit_message(content='Request cancelled.', view=None, embed=None)
        return

    cancel_button = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.red)
    cancel_button.callback = cancel_function
    view.add_item(cancel_button)
