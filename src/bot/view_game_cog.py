from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.core.game_engine import GameEngine


class ViewGameCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='view.events', aliases=['events'])
    async def view_events(self, ctx, *args):
        response = self.engine.view_events(ctx.guild.id)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return
        embed = self.custom_embed(
            'List of Events', None,
            self.events_to_fields(response.response['events'], True)
        )
        await ctx.send(embed=embed)

    @commands.command(name='view.progress', aliases=['progress'])
    async def view_progress(self, ctx, *args):
        print(f'finishing game server_id = {ctx.guild.id}')
        response = self.engine.finish_game(ctx.guild.id)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return
