import discord


class Whoami:
    """
    Description: ?
    """

    def __init__(self, tree, guild, kwargs=None):
        """
        Description: Constructor.
        """

        @tree.command(
            name="whoami",
            description="?",
            guild=discord.Object(id=guild),
        )
        async def whoami(interaction: discord.Interaction):
            """
            /add whoami
            """
            
            await interaction.response.defer()
            
            image = discord.File("./BOT/slash_assets/whoami.png", description="whoami")

            await interaction.followup.send(file=image)