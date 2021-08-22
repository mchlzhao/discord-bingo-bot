from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.bot.util import (
    char_to_index, index_to_emoji)
from src.core.game_engine import GameEngine


class EventHittingCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='hit')
    async def hit(self, ctx, *args):
        server_id = str(ctx.guild.id)
        search_str = ' '.join(args)
        if len(search_str) == 1 and search_str.isalpha():
            response = self.engine.hit(
                server_id, index=char_to_index(search_str))
        else:
            response = self.engine.hit(server_id, desc=search_str)
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        event = response.response['event']
        embed = self.custom_embed(
            '🎯 Event Hit!',
            f'Event {index_to_emoji(event.index)}: {event.desc}'
        )
        await ctx.send(embed=embed)

    @commands.command(name='unhit')
    async def unhit(self, ctx, *args):
        server_id = str(ctx.guild.id)
        search_str = ' '.join(args)
        if len(search_str) == 1 and search_str.isalpha():
            response = self.engine.unhit(
                server_id, index=char_to_index(search_str))
        else:
            response = self.engine.unhit(server_id, desc=search_str)
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        event = response.response['event']
        embed = self.custom_embed(
            '🗑️ Event Unhit!',
            f'Event {index_to_emoji(event.index)}: {event.desc}'
        )
        await ctx.send(embed=embed)
