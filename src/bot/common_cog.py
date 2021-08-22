from typing import List, Tuple, Optional

import discord
from discord.ext import commands

from src.bot.util import ERROR_EMOJI, SPACER_EMOJI, index_to_emoji, hit_emoji
from src.entities.combo_set import ComboSet
from src.entities.event import Event


class CommonCog:
    def custom_embed(self, title: str, desc: Optional[str],
                     fields: List[Tuple[str, str]] = [],
                     inline=True) -> discord.Embed:
        if desc is None:
            embed = discord.Embed(title=title, colour=discord.Colour.blue())
        else:
            embed = discord.Embed(title=title, description=desc,
                                  colour=discord.Colour.blue())
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def display_error_reply(self, ctx: commands.Context,
                                  error_message: str) -> None:
        embed = discord.Embed(
            title=f'{ERROR_EMOJI} Error', description=error_message,
            colour=discord.Colour.dark_red())
        await ctx.message.reply(embed=embed)

    def events_to_fields(self, events: List[Event],
                         include_is_hit: bool) -> List[Tuple[str, str]]:
        fields = []
        for event in events:
            name = f'Event {index_to_emoji(event.index)}'
            if include_is_hit:
                name = f'{hit_emoji(event.is_hit)} - ' + name
            value = event.desc
            fields.append((name, value))
        return fields

    def combo_set_to_emoji(self, combo_set: ComboSet) -> Tuple[str, str]:
        combo_event_strs = []
        combo_hit_strs = []
        for combo in combo_set.combos:
            event_str = ''.join([index_to_emoji(event.index)
                                 for event in combo.events])
            hit_str = ''.join([hit_emoji(event.is_hit)
                               for event in combo.events])
            combo_event_strs.append(event_str)
            combo_hit_strs.append(hit_str)
        return (SPACER_EMOJI.join(combo_event_strs),
                SPACER_EMOJI.join(combo_hit_strs))
