import discord
from discord.ext import commands

from src.bot.util import ERROR_EMOJI


class DisplayError(commands.CommandError):
    def __init__(self, message: str):
        self.error_message = message

    def get_embed(self):
        return discord.Embed(
            title=f'{ERROR_EMOJI} Error', description=self.error_message,
            colour=discord.Colour.dark_red())
