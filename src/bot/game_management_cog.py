from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.bot.util import (
    to_ordinal_with_podium_emoji, COMBO_SIZE, NUM_COMBOS, MAX_EVENTS)
from src.core.game_engine import GameEngine


class GameManagementCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='game.start',
                      aliases=['start', 'game.begin', 'begin'])
    async def start_game(self, ctx, *args):
        event_strs = list(map(str, args))
        if len(event_strs) > MAX_EVENTS:
            await self.display_error_reply(
                ctx, f'There can only be up to {MAX_EVENTS} events.')
            return
        response = self.engine.start_game(str(ctx.guild.id), event_strs)
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return
        embed = self.custom_embed(
            '🚀 Game has Started!',
            f'Choose {NUM_COMBOS} combos of {COMBO_SIZE} events from the following:',
            self.events_to_fields(response.response['events'], False)
        )
        await ctx.send(embed=embed)

    @commands.command(name='game.finish',
                      aliases=['finish', 'game.end', 'end'])
    async def end_game(self, ctx):
        # TODO: present confirmation prompt
        response = self.engine.finish_game(str(ctx.guild.id))
        if response.display_error is not None:
            await self.display_error_reply(ctx, response.display_error)
            return

        # TODO: show podium, final events and progress
        embed = self.custom_embed(
            '🏁 Game has Finished!',
            'Thank you for playing! 💙'
        )
        if len(response.response['entries']) > 0:
            podium_text = [f'<@{entry.player_id}>'
                           for entry in response.response['entries']]
            podium_text = [f'{to_ordinal_with_podium_emoji(i + 1)}: {text}'
                           for i, text in enumerate(podium_text)]
            embed.add_field(name='Here are the winners:\n',
                            value='\n'.join(podium_text))
        else:
            embed.add_field(name='Here are the winners:\n',
                            value='There were no winners :cry:')
        await ctx.send(embed=embed)
