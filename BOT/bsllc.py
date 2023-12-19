"""
DISCORD BOT

Authors: Nolan Gregory, Ethan Christensen, Klim F.
Version: 0.69
Intent: This multifaceted bot is to promote user activity within
        servers that it is hosted in.
"""

import os
import discord
import asyncio
from discord import Message, app_commands
from discord.ext import commands
from slash_master import SlashMaster

class BSLLCBot(discord.Client):
    """
    Desription: Multipurpose discord bot
    """

    def __init__(self, guild, cmds_path, *, debug, intents: discord.Intents, **options):
        super().__init__(intents=intents, **options)

        # Guild ID the bot will only work in
        self.guild = int(guild)
        self.debug = bool(int(debug))
        self.slash_commands_path = cmds_path
        self.globals = {
        }
        # Create CommandTree object
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        """
        Description: Called when the bot is initialized (turned on)
        """

        # get the text channels in the guild
        guild = self.get_guild(self.guild)
        text_channels = None if not guild else guild.text_channels
        
        # tell slash master to load commands
        SlashMaster(self.tree, self.guild, self.slash_commands_path, self.debug).load_commands(
            args=(text_channels,)
        )
