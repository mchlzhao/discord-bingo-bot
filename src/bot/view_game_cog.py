from discord.ext import commands

from src.bot.base_cog import BaseCog
from src.bot.display_error import DisplayError
from src.bot.embed_generator import EmbedGenerator
from src.core.game_engine import GameEngine


class ViewGameCog(BaseCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='view.events', aliases=['events'])
    async def view_events(self, ctx):
        response = self.engine.view_events(str(ctx.guild.id))
        if response.display_error is not None:
            raise DisplayError(response.display_error)
        await ctx.send(
            embed=EmbedGenerator.get_events_embed(response.response['events']))

    @commands.command(name='view.progress', aliases=['progress'])
    async def view_progress(self, ctx, *args):
        # TODO: view progress for specific players
        response = self.engine.view_progress(str(ctx.guild.id))
        if response.display_error is not None:
            raise DisplayError(response.display_error)
        combo_sets = response.response['combo_sets']
        combo_sets_named = [(
            (await ctx.guild.fetch_member(combo_set.player_id)).display_name,
            combo_set) for combo_set in combo_sets]
        combo_sets_named.sort(key=lambda t: t[0].lower())
        await ctx.send(
            embed=EmbedGenerator.get_progress_embed(
                combo_sets_named, response.response['game_has_started']))
