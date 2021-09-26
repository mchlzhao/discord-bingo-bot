from typing import List, Tuple

import discord

from src.bot.util import index_to_emoji, COMBO_SIZE, NUM_COMBOS, \
    to_ordinal_with_podium_emoji, hit_emoji, SPACER_EMOJI, HIDDEN_EMOJI
from src.entities.combo_set import ComboSet
from src.entities.entry import Entry
from src.entities.event import Event


def get_content_embed(**kwargs):
    return discord.Embed(colour=discord.Colour.blue(), **kwargs)


def get_error_embed(**kwargs):
    return discord.Embed(colour=discord.Colour.dark_red(), **kwargs)


def get_event_str(event: Event):
    return f'Event {index_to_emoji(event.index)}: {event.desc}'


def combo_set_to_emoji(combo_set: ComboSet) -> Tuple[str, str]:
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


class EmbedGenerator:
    @staticmethod
    def _get_podium_text(entries: List[Entry], game_ended: bool):
        if len(entries) > 0:
            winners = [f'<@{entry.player_id}>' for entry in entries]
            podium_text = [f'{to_ordinal_with_podium_emoji(i + 1)}: {winner}'
                           for i, winner in enumerate(winners)]
            podium_text[0] += ' 👑'
            return '\n'.join(podium_text)
        if game_ended:
            return 'There were no winners 😢'
        return 'There are currently no winners 😢'

    @staticmethod
    def get_start_embed(events: List[Event]):
        embed = get_content_embed(
            title='🚀 Game has Started!',
            description=f'Choose {NUM_COMBOS} combos of {COMBO_SIZE} events' +
                        ' from the following:')
        for event in events:
            embed.add_field(name=f'Event {index_to_emoji(event.index)}',
                            value=event.desc, inline=True)
        return embed

    @staticmethod
    def get_end_embed(entries: List[Entry]):
        # TODO: final events and progress
        embed = get_content_embed(
            title='🏁 Game has Finished!',
            description='Thank you for playing! 💙')
        embed.add_field(name='Winners:',
                        value=EmbedGenerator._get_podium_text(entries, True))
        return embed

    @staticmethod
    def get_event_hit_embed(event: Event):
        return get_content_embed(
            title='🎯 Event Hit!' if event.is_hit else '🗑️ Event Unhit!',
            description=get_event_str(event))

    @staticmethod
    def get_bingo_embed(player_id: str):
        # TODO: show the winning board
        return get_content_embed(title='🎊 🥳 🎉 Bingo!',
                                 description=f'<@{player_id}> has just won!')

    @staticmethod
    def get_events_embed(events: List[Event]):
        embed = get_content_embed(title='🎲 List of Events')
        for event in events:
            embed.add_field(
                name=f'{hit_emoji(event.is_hit)} - ' +
                     f'Event {index_to_emoji(event.index)}',
                value=event.desc,
                inline=True
            )
        return embed

    @staticmethod
    def get_progress_embed(combo_sets_named: List[Tuple[str, ComboSet]],
                           game_has_started: bool, users_specified: bool):
        embed = get_content_embed(title='🎲 Player Progress')
        if len(combo_sets_named) == 0:
            embed.description = 'No players{} have set an entry{}.'.format(
                ' specified' if users_specified else '',
                ' yet' if not game_has_started else '')
            return embed

        for name, combo_set in combo_sets_named:
            combo_set_emojis = combo_set_to_emoji(combo_set)
            if game_has_started:
                entry = '\n'.join(combo_set_emojis)
            else:
                # this is known to render incredibly large on mobile if the
                # number of total emojis is small
                hidden_emojis = SPACER_EMOJI.join(
                    [''.join([HIDDEN_EMOJI * len(combo.events)])
                     for combo in combo_set.combos])
                entry = f'{hidden_emojis}\n{combo_set_emojis[1]}'
            embed.add_field(name=name, value=entry, inline=False)
        return embed

    @staticmethod
    def get_winners_embed(entries: List[Entry]):
        return get_content_embed(
            title='🏆 Winners',
            description=EmbedGenerator._get_podium_text(entries, False))

    @staticmethod
    def get_help_embed(desc: str):
        return get_content_embed(
            title='🎲 BingoBot Help',
            description=desc)

    @staticmethod
    def get_error_embed(error_message: str):
        return get_error_embed(
            title='❌ Error',
            description=error_message)
