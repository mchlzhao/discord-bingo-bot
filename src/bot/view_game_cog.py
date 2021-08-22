from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.bot.util import HIDDEN_EMOJI, SPACER_EMOJI, NUM_COMBOS, COMBO_SIZE
from src.core.game_engine import GameEngine


class ViewGameCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='view.events', aliases=['events'])
    async def view_events(self, ctx):
        response = self.engine.view_events(str(ctx.guild.id))
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        embed = self.custom_embed(
            '🎲 List of Events', None,
            self.events_to_fields(response.response['events'], True)
        )
        await ctx.send(embed=embed)

    @commands.command(name='view.progress', aliases=['progress'])
    async def view_progress(self, ctx, *args):
        # TODO: view progress for specific players
        response = self.engine.view_progress(str(ctx.guild.id))
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        combo_sets = response.response['combo_sets']
        combo_sets_named = [
            ((await ctx.guild.fetch_member(combo_set.player_id)).display_name,
             combo_set) for combo_set in combo_sets]
        combo_sets_named.sort(key=lambda t: t[0].lower())
        fields = []
        for name, combo_set in combo_sets_named:
            combo_set_emojis = self.combo_set_to_emoji(combo_set)
            if response.response['game_has_started']:
                fields.append(
                    (name, '\n'.join(combo_set_emojis)))
            else:
                hidden_emojis = SPACER_EMOJI.join(
                    [HIDDEN_EMOJI * COMBO_SIZE] * NUM_COMBOS)
                fields.append(
                    (name, hidden_emojis + '\n' + combo_set_emojis[1]))
        if len(fields) == 0:
            desc = 'No players have set an entry yet.'
        else:
            desc = None
        embed = self.custom_embed(
            '🎲 Player Progress', desc,
            fields,
            inline=False
        )
        await ctx.send(embed=embed)
