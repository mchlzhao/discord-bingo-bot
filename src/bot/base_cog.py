from discord.ext import commands

from src.bot.display_error import DisplayError
from src.bot.embed_generator import EmbedGenerator


class BaseCog(commands.Cog):
    async def cog_command_error(self, ctx, error):
        if isinstance(error, DisplayError):
            await ctx.message.reply(embed=EmbedGenerator.get_error_embed(error))
        else:
            raise error
