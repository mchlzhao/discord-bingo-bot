import discord
from discord.ext import commands

from core.Game import Game

SUCCESS_EMOJI = '👍'
FAILURE_EMOJI = '👎'
ERROR_EMOJI = '❌'
HIT_EMOJI = '🟢'
UNHIT_EMOJI = '🔴'
HIDDEN_EMOJI = '❔'

def char_to_emoji(c):
    return f':regional_indicator_{c.lower()}:'

def str_to_emoji(s):
    return ''.join(map(char_to_emoji, s))

def index_to_char(i):
    return chr(ord('A') + i)

def char_to_index(c):
    return ord(c) - ord('A')

def index_to_emoji(i):
    return char_to_emoji(index_to_char(i))

def indices_to_emoji(l):
    return ''.join(map(index_to_emoji, l))

def bool_to_emoji(b):
    return HIT_EMOJI if b else UNHIT_EMOJI

def mask_to_emoji(m):
    return ''.join(map(bool_to_emoji, m))

def get_name(member):
    return member.nick or member.name



bot = commands.Bot(command_prefix='<>')
game = None

@bot.event
async def on_ready():
    global game
    print('Bot ready')
    game = Game('Test Game', None)
    game.set_events([
        '> Lights out and away we go',
        '> Down the inside/round the outside',
        'MazesBin DNFs'
    ] + [f'Event {i}' for i in range(4, 11)])
    game.set_player(740728443611775006, list(range(10)))

@bot.command(name='test')
async def test_command(ctx):
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    await ctx.message.reply('hello')

@bot.command(aliases=['quit'])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await bot.close()
    print('Bot Closed')



@bot.command(name='view_events')
async def view_events(ctx):
    embed = discord.Embed(title='List of Events:')
    for ind, event in enumerate(game.events):
        embed.add_field(
            name=f'Event {index_to_emoji(event.index)}: {bool_to_emoji(event.is_hit)}',
            value=event.desc,
            inline=False
        )
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    await ctx.send(embed=embed)

@bot.command(name='view_progress')
async def view_progress(ctx, *args):
    print('<>view_progress', args)
    embed = discord.Embed(title='Player Progress:')
    for player_id, entry in game.players.items():
        member = await ctx.guild.fetch_member(player_id)
        mask = entry.get_mask(game.events_hit)
        board = indices_to_emoji(entry.board) if game.has_game_started() else HIDDEN_EMOJI * len(game.events)
        embed.add_field(
            name=get_name(member),
            value=f'{board}\n{mask_to_emoji(mask)}',
            inline=False
        )
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    await ctx.send(embed=embed)



def labelled_message(label, message, emoji=None):
    if emoji:
        return f'{emoji} {label}: {message}'
    return f'{label}: {message}'

async def error_reply(ctx, error_message):
    await ctx.message.add_reaction(FAILURE_EMOJI)
    await ctx.message.reply(labelled_message('ERROR', error_message, ERROR_EMOJI))



@bot.command(name='set_board')
async def set_board_command(ctx, *args):
    # remove all newlines, extraneous characters
    chars = map(lambda x: [y for y in x], args)
    chars = [c for sublist in chars for c in sublist]
    chars = list(filter(str.isalpha, chars))

    # need to ensure all indices 1 to n are featured exactly once
    is_valid = sorted(chars) == sorted(list(map(index_to_char, range(len(game.events)))))
    game_started = game.has_game_started()
    if game_started:
        await error_reply(ctx, 'Cannot set board when game has started')
    elif not is_valid:
        await error_reply(ctx, f'Your board is not a permutation of the events A-{index_to_char(len(game.events)-1)}')
    else:
        board_order = list(map(char_to_index, chars))
        game.set_player(str(ctx.author.id), board_order)
        await ctx.message.add_reaction(SUCCESS_EMOJI)



def search_events(s):
    matches = []
    for event in game.events:
        if s.lower() in event.desc.lower():
            matches.append(event)
    return matches

async def generic_hit(ctx, search_string):
    search_results = search_events(search_string)
    if search_string.isalpha() and len(search_string) == 1:
        try:
            index = ord(search_string.upper()) - ord('A')
            search_results = [game.events[index]]
        except IndexError:
            await error_reply(ctx, f'Event index must be between A-{index_to_char(len(game.events)-1)}')
            return None
    if len(search_results) == 0:
        await error_reply(ctx, f'No event matches "{search_string}"')
        return None
    if len(search_results) > 1:
        error_str = f'More than one event matches "{search_string}"\n'
        error_str += f'Matches include: "{search_results[0].desc}", "{search_results[1].desc}"'
        if len(search_results) > 2:
            error_str += ', ...'
        await error_reply(ctx, error_str)
        return None
    return search_results[0]

@bot.command(name='hit')
async def hit(ctx, *args):
    search_string = ' '.join(args)
    event = await generic_hit(ctx, search_string)
    if event is None:
        return
    if event.is_hit:
        await error_reply(ctx, 'Event is already hit')
        return
    game.hit(event.index)
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    await ctx.send(labelled_message('HIT', f'Event {index_to_char(event.index)} "{event.desc}"', HIT_EMOJI))

@bot.command(name='unhit')
async def unhit(ctx, *args):
    search_string = ' '.join(args)
    event = await generic_hit(ctx, search_string)
    if event is None:
        return
    if not event.is_hit:
        await error_reply(ctx, 'Event is already unhit')
        return
    game.unhit(event.index)
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    await ctx.send(labelled_message('UNHIT', f'Event {index_to_char(event.index)} "{event.desc}"', UNHIT_EMOJI))
