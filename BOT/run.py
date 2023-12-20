import os

import discord
from dotenv import load_dotenv
from bsllc import BSLLCBot


def main():
    """
    Description: Invoke the bot and prepare the tokens.
    """
    load_dotenv(override=True)

    token = os.environ["TOKEN"]
    guild = os.environ["GUILD_ID"]
    cmds_path = os.environ["SLASH_COMMANDS_PATH"]
    debug = os.environ["DEBUG"]

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.voice_states = True

    bot = BSLLCBot(guild, cmds_path, debug=debug, intents=intents)
    bot.run(token)


if __name__ == "__main__":
    main()
