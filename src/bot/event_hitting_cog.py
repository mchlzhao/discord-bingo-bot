from discord.ext import commands

from src.bot.base_cog import BaseCog
from src.bot.display_error import DisplayError
from src.bot.embed_generator import EmbedGenerator
from src.bot.util import char_to_index
from src.core.game_engine import GameEngine
from src.entities.event import Event


class EventHittingCog(BaseCog, name='Event Hitting'):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    def change_hit(self, is_hit: bool, ctx, *args) -> Event:
        server_id = str(ctx.guild.id)
        search_str = ' '.join(args)
        if len(search_str) == 0:
            raise DisplayError('No search term provided.')
        if len(search_str) == 1 and search_str.isalpha():
            response = self.engine.change_hit(
                server_id, is_hit, index=char_to_index(search_str))
        else:
            response = self.engine.change_hit(server_id, is_hit,
                                              desc=search_str)
        if response.display_error is not None:
            raise DisplayError(response.display_error)
        return response.response['event']

    @commands.command(name='hit',
                      description='Check off an event when it has occurred.',
                      usage='<event index|desc substring>')
    async def hit(self, ctx, *args):
        event = self.change_hit(True, ctx, *args)
        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(event))

    @commands.command(name='unhit',
                      description='Undo the hitting of an event.',
                      usage='<event index|desc substring>')
    async def unhit(self, ctx, *args):
        event = self.change_hit(False, ctx, *args)
        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(event))
