import discord
from discord.app_commands import Group

class Sync(Group):
    def __init__(self, tree, guild, args=None):
        @tree.command(
            name="sync", description="Owner only", guild=discord.Object(id=guild)
        )
        async def sync(interaction: discord.Interaction):
            await interaction.response.defer()
            try:
                await tree.sync(guild=discord.Object(id=guild))
            except:
                pass

            await interaction.followup.send(content="Synced commands.")