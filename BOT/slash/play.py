import asyncio
import discord
import utils.ytdl as yt
from discord import VoiceProtocol


class Play:
    """
    Description: command to play audio from a link or search query.
    """

    def __init__(self, tree: discord.app_commands.CommandTree, guild: discord.Guild, kwargs: dict[str, any] = None):
        """
        Description: Constructor.
        """

        async def load_song(song: str, interaction: discord.Interaction):
            return await yt.YTDLSource.from_url(song)

        async def regather_stream(file_dict: dict):
            return await yt.YTDLSource.regather_stream(file_dict["webpage"])

        @tree.command(
            name="play",
            description="play audio from a link or search query",
            guild=discord.Object(id=guild),
        )
        async def play(interaction: discord.Interaction, query_or_link: str):
            """
            /play command
            command to play audio from a link or search query
            """

            await interaction.response.defer()

            if interaction.user.voice is None:
                await interaction.followup.send(content="You are not in a voice channel.")
            else:
                user_voice_channel = interaction.user.voice.channel
                bot_voice_channel = discord.utils.get(
                    interaction.client.voice_clients, guild=interaction.guild)

                if not bot_voice_channel:
                    channel = await user_voice_channel.connect()
                else:
                    channel = interaction.guild.voice_client

                if interaction.guild.voice_client is not None:
                    if channel.is_playing() or channel.is_paused():
                        interaction.client.globals.get(
                            "queue").append(query_or_link)
                        await interaction.followup.send(content="Song added to queue.")
                    else:
                        file = await load_song(query_or_link, interaction=interaction)
                        source = await regather_stream(file)
                        audio_player = discord.FFmpegPCMAudio(
                            executable="ffmpeg",
                            before_options=(
                                "-reconnect 1 -reconnect_streamed 1"
                                " -reconnect_delay_max 5"
                            ),
                            options=(
                                f'-vn -filter_complex "aecho=1.0:0.7:30:0.5, aresample=48000, asetrate=48000*0.85, compand=attacks=0:points=-80/-169|-54/-80|-49.5/-64.6|-41.1/-41.1|-25.8/-15|-10.8/-4.5|0/0|20/8.3"'
                            ),
                            source=source,
                        )

                        channel.play(
                            audio_player,
                            after=lambda x: (
                                print(f"ERROR: {x}")
                                if x
                                else play_next(channel, interaction, audio_player)
                            ),
                        )

                        await interaction.followup.send(content="Playing audio.")

        def play_next(
            channel: VoiceProtocol,
            interaction: discord.Interaction,
            player: discord.FFmpegAudio,
        ):
            queue = interaction.client.globals.get("queue")

            if len(queue) > 0:
                next_song = queue.pop(0)
                channel.stop()
                player._kill_process()
                file_dict = asyncio.run(
                    load_song(next_song, interaction=interaction))
                source = asyncio.run(regather_stream(file_dict))
                interaction.client.loop.create_task(
                    interaction.channel.send(content="Playing next song.")
                )

                audio_player = discord.FFmpegPCMAudio(
                    executable="ffmpeg",
                    before_options=(
                        "-reconnect 1 -reconnect_streamed 1"
                        " -reconnect_delay_max 5"
                    ),
                    options=(
                        f'-vn -filter_complex "aecho=1.0:0.7:30:0.5, aresample=48000, asetrate=48000*0.85, compand=attacks=0:points=-80/-169|-54/-80|-49.5/-64.6|-41.1/-41.1|-25.8/-15|-10.8/-4.5|0/0|20/8.3"'
                    ),
                    source=source
                )

                channel.play(
                    audio_player,
                    after=lambda x: (
                        print(f"ERROR: {x}")
                        if x
                        else play_next(channel, interaction, audio_player)
                    ),
                )
            else:
                interaction.client.loop.create_task(
                    interaction.channel.send(content="Queue is empty.")
                )
