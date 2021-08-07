import discord
from discord.ext import commands
from typing import List, Tuple

from src.bot.util import ERROR_EMOJI, index_to_emoji, hit_emoji
from src.entities.event import Event


class CommonCog:
    def custom_embed(self, title: str, desc: str,
                     fields: List[Tuple[str, str]] = [], inline=True):
        if desc is None:
            embed = discord.Embed(title=title, colour=discord.Colour.blue())
        else:
            embed = discord.Embed(title=title, description=desc,
                                  colour=discord.Colour.blue())
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def display_error_response(self, ctx: commands.Context,
                                     error_message: str):
        embed = discord.Embed(
            title=f'{ERROR_EMOJI} Error', description=error_message,
            colour=discord.Colour.dark_red())
        await ctx.message.reply(embed=embed)

    def events_to_fields(self, events: List[Event], include_is_hit: bool):
        fields = []
        for event in events:
            name = f'Event {index_to_emoji(event.index)}'
            if include_is_hit:
                name = f'{hit_emoji(event.is_hit)} - ' + name
            value = event.desc
            fields.append((name, value))
        return fields
