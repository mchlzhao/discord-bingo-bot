import discord
from discord.ext import commands

from core.Game import Game


SUCCESS_EMOJI = '👍'
FAILURE_EMOJI = '👎'

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
    return ':white_check_mark:' if b else ':black_circle:'

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
        '"Lights out and away we go"',
        '"Down the inside/round the outside',
        'MazesBin DNFs'
    ])
    game.set_player(740728443611775006, [2, 1, 0])

@bot.command(name='test')
async def test_command(ctx):
    await ctx.send('hello')

@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await bot.close()
    print("Bot Closed")



@bot.command(name='view_events')
async def view_events(ctx):
    embed = discord.Embed(title='List of Events:')
    for ind, event in enumerate(game.events):
        embed.add_field(
            name='Event ' + index_to_emoji(event.index),
            value=event.desc,
            inline=False
        )
    await ctx.send(embed=embed)

@bot.command(name='view_progress')
async def view_progress(ctx, *args):
    print('<>view_progress', args)
    embed = discord.Embed(title='Player Progress:')
    for player_id, entry in game.players.items():
        member = ctx.guild.get_member(player_id)
        mask = entry.get_mask(game.events_hit)
        embed.add_field(
            name=get_name(member),
            value=indices_to_emoji(entry.board) + '\n' + mask_to_emoji(mask),
            inline=False
        )
    await ctx.send(embed=embed)

@bot.command(name='set_board')
async def set_board_command(ctx, *args):
    # remove all newlines, extraneous characters
    chars = map(lambda x: [y for y in x], args)
    chars = [c for sublist in chars for c in sublist]
    chars = list(filter(str.isalpha, chars))

    # need to ensure all indices 1 to n are featured exactly once
    is_valid = sorted(chars) == sorted(list(map(index_to_char, range(len(game.events)))))
    if is_valid:
        board_order = list(map(char_to_index, chars))
        game.set_player(ctx.author.id, board_order)
        await ctx.message.add_reaction(SUCCESS_EMOJI)
    else:
        await ctx.message.add_reaction(FAILURE_EMOJI)
        await ctx.send(f'ERROR <@{ctx.author.id}>: Your board is not a permutation of the events')
