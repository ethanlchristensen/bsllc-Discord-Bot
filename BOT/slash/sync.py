import discord
from discord.app_commands import Group

class Sync(Group):
    def __init__(self, tree, guild, kwargs=None):
        @tree.command(
            name="sync", description="Owner only", guild=discord.Object(id=guild)
        )
        async def sync(interaction: discord.Interaction):
            await interaction.response.defer()
            if interaction.user.global_name == "etchris":
                try:
                    await tree.sync(guild=discord.Object(id=guild))
                except:
                    pass
            else:
                print(f"User {interaction.user} is not owner.")

            await interaction.followup.send(content="Synced commands.")