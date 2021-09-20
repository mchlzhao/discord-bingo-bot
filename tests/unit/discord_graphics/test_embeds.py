from datetime import datetime

from discord.ext import commands

from src.bot.display_error import DisplayError
from src.bot.embed_generator import EmbedGenerator
from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event


class TestEmbedsCog(commands.Cog):
    @commands.command(name='test_embeds')
    async def test_embeds(self, ctx):
        events = [Event(0, 0, 'Event1', 0), Event(1, 0, 'Event2', 1),
                  Event(2, 0, 'Event3', 2)]
        await ctx.send(embed=EmbedGenerator.get_start_embed(events))
        entries = [Entry(0, 0, 'Player1', datetime.now()),
                   Entry(1, 0, 'Player2', datetime.now()),
                   Entry(2, 0, 'Player3', datetime.now()),
                   Entry(3, 0, 'Player4', datetime.now())]
        await ctx.send(embed=EmbedGenerator.get_end_embed(entries))
        await ctx.send(embed=EmbedGenerator.get_end_embed([]))

        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(events[0]))
        events[0].is_hit = True
        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(events[0]))

        await ctx.send(embed=EmbedGenerator.get_bingo_embed('Player1'))

        await ctx.send(embed=EmbedGenerator.get_events_embed(events))

        combo_set = ComboSet('Player1', [Combo(0, events, 0),
                                         Combo(1, events, 1)])
        combo_sets_named = [('Player1', combo_set), ('Player2', combo_set)]
        await ctx.send(
            embed=EmbedGenerator.get_progress_embed(combo_sets_named, True))
        await ctx.send(
            embed=EmbedGenerator.get_progress_embed(combo_sets_named, False))

        await ctx.send(embed=EmbedGenerator.get_error_embed(
            DisplayError('This is a sample error')))
