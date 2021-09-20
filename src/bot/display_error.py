from discord.ext import commands


class DisplayError(commands.CommandError):
    def __init__(self, message: str):
        self.error_message = message
