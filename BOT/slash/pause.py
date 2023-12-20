import discord
from discord.app_commands import Group


class Pause(Group):
    def __init__(self, tree, guild, kwargs=None):
        @tree.command(
            description="Pause  the currently playing song.", name="pause", guild=discord.Object(id=guild)
        )
        async def pause(interaction: discord.Interaction):
            """
            Pause the currently playing song
            """

            user_channel = interaction.user.voice

            voice_channel = interaction.guild.voice_client

            await interaction.response.defer()

            if user_channel:
                if voice_channel:
                    if voice_channel.is_playing():

                        voice_channel.pause()

                        await interaction.followup.send(content="Paused the song!")

                    else:
                        await interaction.followup.send(content="No song is currently playing.")
