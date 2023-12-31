"""
When a new slash command file is made, add it here
Also add it in self._slash_commands list
"""

import os
from sys import platform

from utils.alterts import (
    DateTimeAlert,
    SuccessAlert,
    ErrorAlert
)


class SlashMaster:
    """
    responsible for loading in each command
    """

    def __init__(self, tree, guild, path, debug):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            self.path = os.path.dirname(__file__) + "/" + path
        else:
            self.path = os.path.dirname(__file__) + "\\" + path

        self.debug = debug
        self.tree = tree
        self.guild = guild

    def load_commands(self, kwargs=None):
        """
        initialize each command with the current tree and guild
        """
        for file in self.get_next_command():
            print(
                DateTimeAlert(
                    f"loading {file:^10s} . . . ",
                    dtia_alert_type="INFO",
                    message_from="BOT.slash_master",
                ).text,
                end="",
            )
            try:
                file_capitalized = "".join(
                    [word.capitalize() for word in file.split("_")]
                )
                pre_loaded_command = self.import_from(
                    f"slash.{file}", file_capitalized
                )
                pre_loaded_command = pre_loaded_command(
                    self.tree, self.guild, kwargs=kwargs
                )
                print(f"{SuccessAlert('success')}")
            except Exception as error:
                print(f"{ErrorAlert('failure')}\n └─ {str(error)}")

    def get_next_command(self):
        """
        Description: TODO
        """
        for file in os.listdir(self.path):
            if "__" not in file and "error" not in file:
                yield file[:-3]

    @staticmethod
    def import_from(module, name):
        """
        Description: TODO
        """
        module = __import__(module, fromlist=[name])
        return getattr(module, name)
