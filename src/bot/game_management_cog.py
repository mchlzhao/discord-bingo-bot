from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.core.game_engine import GameEngine


class GameManagementCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='game.start')
    async def start_game(self, ctx, *args):
        # TODO: check no more than 26 events
        event_strs = args
        print(
            f'starting game server_id = {ctx.guild.id}, events = {event_strs}')
        response = self.engine.start_game(ctx.guild.id, event_strs)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return
        embed = self.custom_embed(
            '🎲 Game Starting!',
            'Choose from the following events:',
            self.events_to_fields(response.response['events'], False)
        )
        await ctx.send(embed=embed)

    @ commands.command(name='game.finish')
    async def end_game(self, ctx, *args):
        print(f'finishing game server_id = {ctx.guild.id}')
        response = self.engine.finish_game(ctx.guild.id)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return

        # TODO: show podium, final events and progress
