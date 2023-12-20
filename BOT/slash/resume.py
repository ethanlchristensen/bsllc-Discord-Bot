import discord
from discord.app_commands import Group


class Resume(Group):
    def __init__(self, tree, guild, kwargs=None):
        @tree.command(
            description="Resume a song", name="resume", guild=discord.Object(id=guild)
        )
        async def resume(interaction: discord.Interaction):
            """
            Resume a song that was paused.
            """
            # grab the channel the user is in
            user_channel = interaction.user.voice
            # grab the channel the bot is in
            voice_channel = interaction.guild.voice_client
            await interaction.response.defer()
            if user_channel:
                if voice_channel: 
                    if voice_channel.is_paused():
                        voice_channel.resume()
                        await interaction.followup.send(content="Resumed the song!")
                    elif voice_channel.is_playing():
                        await interaction.followup.send(content="No song is currently paused.")
                    else:
                        await interaction.followup.send(content="No song is currently playing.")
                else:
                    await interaction.followup.send(content="I am not connected to a voice channel.")
