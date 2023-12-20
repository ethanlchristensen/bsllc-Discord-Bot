import discord
from discord.app_commands import Group


class Skip(Group):
    def __init__(self, tree, guild, kwargs=None):
        @tree.command(
            description="Skip a song", name="skip", guild=discord.Object(id=guild)
        )
        async def skip(interaction: discord.Interaction):
            """
            skip song from queue.
            """

            # INITIALIZE USER STATUS AND BOT STATUS
            user_channel = interaction.user.voice
            voice_channel = interaction.guild.voice_client

            # AWAIT A RESPONSE
            await interaction.response.defer()

            # IF THE USER IS NOT THE VOICE CHANNEL, ISSUE ERROR
            if not user_channel:
                await interaction.followup.send(
                    content="You are not in a voice channel!"
                )

            # SEE IF THE BOT IS IN THE CHANNEL
            elif voice_channel:
                # If the bot is currently playing music
                if voice_channel.is_playing():
                    # This is BROKEN
                    voice_channel.stop()

                    await interaction.followup.send(
                        content="Song has been skipped!"
                    )
                # If the bot is in the voice channel but no music is playing
                else:
                    await interaction.followup.send(
                        content="Bot is not playing music!"
                    )

            # BOT IS NOT IN THE CHANNEL
            else:
                await interaction.followup.send(
                    content="Bot is not in a voice channel!"
                )
