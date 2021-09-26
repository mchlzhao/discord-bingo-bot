from datetime import datetime

from discord.ext import commands

from src.bot.embed_generator import EmbedGenerator
from src.entities.combo import Combo
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event

events = [Event(0, 0, 'Event1', 0), Event(1, 0, 'Event2', 1),
          Event(2, 0, 'Event3', 2)]
entries = [Entry(0, 0, 'Player1', datetime.now()),
           Entry(1, 0, 'Player2', datetime.now()),
           Entry(2, 0, 'Player3', datetime.now()),
           Entry(3, 0, 'Player4', datetime.now())]
combo_set = ComboSet('Player1', [Combo(0, events, 0),
                                 Combo(1, events, 1)])


class TestEmbedsCog(commands.Cog):
    @commands.command(name='test.start')
    async def test_start(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_start_embed(events))

    @commands.command(name='test.end')
    async def test_end(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_end_embed(entries))
        await ctx.send(embed=EmbedGenerator.get_end_embed([]))

    @commands.command(name='test.hit')
    async def test_hit(self, ctx):
        events[0].is_hit = True
        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(events[0]))
        events[0].is_hit = False

    @commands.command(name='test.unhit')
    async def test_unhit(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_event_hit_embed(events[0]))

    @commands.command(name='test.bingo')
    async def test_bingo(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_bingo_embed('Player1'))

    @commands.command(name='test.events')
    async def test_events(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_events_embed(events))

    @commands.command(name='test.progress')
    async def test_progress(self, ctx):
        combo_sets_named = [('Player1', combo_set), ('Player2', combo_set)]
        await ctx.send(
            embed=EmbedGenerator.get_progress_embed([], True, False))
        await ctx.send(
            embed=EmbedGenerator.get_progress_embed([], False, False))
        await ctx.send(embed=EmbedGenerator.get_progress_embed(
            combo_sets_named, True, False))
        await ctx.send(embed=EmbedGenerator.get_progress_embed(
            combo_sets_named, False, False))

    @commands.command(name='test.winners')
    async def test_winners(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_winners_embed(entries))
        await ctx.send(embed=EmbedGenerator.get_winners_embed([]))

    @commands.command(name='test.help')
    async def test_help(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_help_embed('Help message'))

    @commands.command(name='test.error')
    async def test_error(self, ctx):
        await ctx.send(embed=EmbedGenerator.get_error_embed(
            'This is a sample error'))

    @commands.command(name='test.all')
    async def test_all(self, ctx):
        await self.test_start(ctx)
        await self.test_end(ctx)
        await self.test_hit(ctx)
        await self.test_unhit(ctx)
        await self.test_bingo(ctx)
        await self.test_events(ctx)
        await self.test_progress(ctx)
        await self.test_winners(ctx)
        await self.test_help(ctx)
        await self.test_error(ctx)
