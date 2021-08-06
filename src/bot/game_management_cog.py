from discord.ext import commands

from src.core.game_engine import GameEngine


class GameManagementCog(commands.Cog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='game.start')
    async def start_game(self, ctx, *args):
        event_strs = args
        print(
            f'starting game server_id = {ctx.guild.id}, events = {event_strs}')
        self.engine.start_game(ctx.guild.id, event_strs)

    @commands.command(name='game.finish')
    async def end_game(self, ctx, *args):
        print(f'finishing game server_id = {ctx.guild.id}')
        self.engine.finish_game(ctx.guild.id)
