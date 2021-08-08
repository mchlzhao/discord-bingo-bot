from discord.ext import commands

from src.bot.common_cog import CommonCog
from src.bot.util import to_ordinal_with_podium_emoji
from src.core.game_engine import GameEngine


class GameManagementCog(commands.Cog, CommonCog):
    def __init__(self, bot: commands.Bot, engine: GameEngine):
        self.bot = bot
        self.engine = engine

    @commands.command(name='game.start')
    async def start_game(self, ctx, *args):
        event_strs = args
        if len(event_strs) > 26:
            await self.display_error_response(
                ctx, 'There can only be up to 26 events.')
            return
        response = self.engine.start_game(ctx.guild.id, event_strs)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return
        embed = self.custom_embed(
            '🎲 Game is Starting!',
            'Choose from the following events:',
            self.events_to_fields(response.response['events'], False)
        )
        await ctx.send(embed=embed)

    @ commands.command(name='game.finish')
    async def end_game(self, ctx, *args):
        response = self.engine.finish_game(ctx.guild.id)
        if response.display_error is not None:
            await self.display_error_response(ctx, response.display_error)
            return

        # TODO: show podium, final events and progress
        embed = self.custom_embed(
            '🏁 Game is Finished!',
            'Thank you for playing! 💙'
        )
        if len(response.response['entries']) > 0:
            podium_text = [f'<@{entry.player_id}>'
                           for entry in response.response['entries']]
            podium_text = [f'{to_ordinal_with_podium_emoji(i+1)}: {text}'
                           for i, text in enumerate(podium_text)]
            embed.add_field(name='Here are the winners:\n',
                            value='\n'.join(podium_text))
        else:
            embed.add_field(name='Here are the winners:\n',
                            value='There were no winners :cry:')
        await ctx.send(embed=embed)
