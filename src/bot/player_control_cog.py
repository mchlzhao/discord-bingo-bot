from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.bot.util import (NUM_COMBOS, COMBO_SIZE, char_to_index, SUCCESS_EMOJI)
from src.core.game_engine import GameEngine


class PlayerControlCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='set_entry', aliases=['set', 'entry'])
    async def set_entry(self, ctx, *args):
        # flatten all args into a single list of chars
        event_index_chars = [c for sublist in map(list, args) for c in sublist]
        # remove non alphabetical chars
        event_index_chars = list(filter(str.isalpha, event_index_chars))
        # convert chars to indices from 0
        event_indices = list(map(char_to_index, event_index_chars))

        if len(event_indices) != NUM_COMBOS * COMBO_SIZE:
            await self.display_error_reply(
                ctx,
                f'Entry is invalid: must have {NUM_COMBOS} boards of {COMBO_SIZE}')
            return

        combos = []
        for i in range(0, NUM_COMBOS * COMBO_SIZE, COMBO_SIZE):
            combo_indices = sorted(event_indices[i:i + COMBO_SIZE])
            if combo_indices != sorted(list(set(combo_indices))):
                await self.display_error_reply(
                    ctx,
                    f'Combo {i // COMBO_SIZE + 1} is invalid: Events must be unique.')
                return
            combos.append(combo_indices)
        combos.sort()

        response = self.engine.set_entry(
            str(ctx.guild.id), str(ctx.author.id), combos)
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @commands.command(name='BINGO!')
    async def bingo(self, ctx):
        # TODO: add user cooldown
        response = self.engine.bingo(str(ctx.guild.id), str(ctx.author.id))
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        embed = self.custom_embed(
            '🏆 🥳 🎉 Bingo!',
            f'<@{ctx.author.id}> has just won!'
        )
        # TODO: show the winning board
        await ctx.send(embed=embed)

    @commands.command(name='bingo', aliases=['bingo!', 'BINGO'])
    async def no_bingo(self, ctx):
        await self.display_error_reply(ctx, 'Say it louder! "BINGO!"')
