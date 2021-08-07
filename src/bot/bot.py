import discord
from discord.ext import commands

SUCCESS_EMOJI = '👍'
FAILURE_EMOJI = '👎'
ERROR_EMOJI = '❌'
HIT_EMOJI = '🟢'
UNHIT_EMOJI = '🔴'
SPACER_EMOJI = '▪️'
HIDDEN_EMOJI = '❔'

NUM_COMBOS = 4
COMBO_SIZE = 3

FROM_DAT = True


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


bot = commands.Bot(command_prefix='<>', help_command=None)
game = None


'''
@bot.event
async def on_ready():
    global game
    print('Bot ready')
    game = Game('Test Game', None)
    if FROM_DAT:
        with open('data/events.dat', 'r') as events_file:
            already_hit = []
            event_strs = []
            for line in events_file:
                tokens = line.strip().split('~')
                index = int(tokens[0])
                desc = tokens[1]
                is_hit = tokens[2] == 'True'
                if is_hit:
                    already_hit.append(index)
                event_strs.append(desc)
            game.set_events(event_strs)

        with open('data/players.dat', 'r') as players_file:
            for line in players_file:
                tokens = line.split('~')
                player_id = tokens[0]
                entry = list(map(int, tokens[1:]))
                game.set_player(player_id, entry)

        for i in already_hit:
            game.hit(i)
    else:
        game.set_events([
            '> Lights out and away we go',
            '> Down the inside/round the outside',
            'MazesBin DNFs'
        ] + [f'Event {i}' for i in range(4, 11)])
        game.set_player(740728443611775006, [
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2])
        game.set_player(741134158247755886, [
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2])
        game.set_player(865037902529953793, [
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2])


@bot.command(name='test')
async def test_command(ctx):
    await ctx.message.add_reaction(SUCCESS_EMOJI)


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='Bingo Bot Help:')
    embed.add_field(
        name='<>set_entry [ABC DEF GHI JKL]',
        value=f'Assign {NUM_COMBOS} combos of {COMBO_SIZE} events each. If all {COMBO_SIZE} events occur in any combo, you win. Each event cannot be repeated in a combo, but can be in more than one combo. Entry can be freely changed as long as no event has been hit.',
        inline=False
    )
    embed.add_field(
        name='<>hit [event]',
        value='Hit an event once it has occurred.',
        inline=False
    )
    embed.add_field(
        name='<>unhit [event]',
        value='Unhit an event if it was mistakenly hit.',
        inline=False
    )
    embed.add_field(
        name='<>view_events',
        value='Lists all events to make combos from.',
        inline=False
    )
    embed.add_field(
        name='<>view_progress',
        value='Lists all players, their chosen entries and their progress on each combo. If no event has been hit, entries are kept secret.',
        inline=False
    )
    await ctx.message.reply(embed=embed)


@bot.command(name='view_events')
async def view_events(ctx):
    embed = discord.Embed(title='List of Events:')
    for ind, event in enumerate(game.events):
        embed.add_field(
            name=f'Event {index_to_emoji(event.index)} - {bool_to_emoji(event.is_hit)}:',
            value=f'> {event.desc}'
        )
    await ctx.send(embed=embed)

progress_embed = None


def get_player_progress(player_id):
    entry = game.players[player_id]
    masks = entry.get_masks(game.events_hit_dict)
    mask_str = SPACER_EMOJI.join(map(mask_to_emoji, masks))
    if game.has_started():
        boards = [board.board_order for board in entry.boards]
        board_str = SPACER_EMOJI.join(map(indices_to_emoji, boards))
    else:
        boards = [HIDDEN_EMOJI * COMBO_SIZE] * NUM_COMBOS
        board_str = SPACER_EMOJI.join(boards)
    return (board_str, mask_str)


@bot.command(name='view_progress')
async def view_progress(ctx, *args):
    global progress_embed
    if progress_embed is None:
        progress_embed = discord.Embed(title='Player Progress:')
        for player_id in game.players:
            member = await ctx.guild.fetch_member(player_id)
            board_str, mask_str = get_player_progress(player_id)
            progress_embed.add_field(
                name=get_name(member),
                value=f'> {board_str}\n> {mask_str}',
                inline=False
            )
    await ctx.send(embed=progress_embed)


def save_game_to_file():
    with open('data/events.dat', 'w') as events_file:
        for event in game.events:
            print(
                '~'.join(map(str, (event.index, event.desc, event.is_hit))),
                file=events_file
            )
    with open('data/players.dat', 'w') as players_file:
        for player_id, entry in game.players.items():
            entry_order = []
            for board in entry.boards:
                entry_order.extend(board.board_order)
            print(
                '~'.join(map(str, [player_id] + entry_order)),
                file=players_file
            )


def labelled_message(label, message, emoji=None):
    if emoji:
        return f'{emoji} {label}: {message}'
    return f'{label}: {message}'


def embed_title(title, emoji):
    return f'{emoji} {title} {emoji}'


async def error_reply(ctx, error_message):
    embed = discord.Embed(title=embed_title(
        'Error', ERROR_EMOJI), description=error_message)
    await ctx.message.reply(embed=embed)


@bot.command(name='set_entry')
async def set_entry_command(ctx, *args):
    if game.has_started():
        await error_reply(ctx, 'Cannot set board when game has already started')
        return

    # remove all newlines, extraneous characters
    chars = map(lambda x: [y for y in x], args)
    chars = [c for sublist in chars for c in sublist]
    chars = list(filter(str.isalpha, chars))

    if len(chars) != NUM_COMBOS * COMBO_SIZE:
        await error_reply(ctx, f'Entry is invalid: must have {NUM_COMBOS} boards of {COMBO_SIZE}')
        return

    # need to ensure all indices 1 to n are featured exactly once
    entry_order = []
    for i in range(0, NUM_COMBOS * COMBO_SIZE, COMBO_SIZE):
        board = sorted(list(map(char_to_index, chars[i:i + COMBO_SIZE])))
        if board != sorted(list(set(board))):
            await error_reply(ctx, f'Multi {i // COMBO_SIZE + 1} is invalid: events in a board must be unique')
            return
        if max(board) >= len(game.events):
            await error_reply(ctx, f'Multi {i // COMBO_SIZE + 1} is invalid: event indices must be between A-{index_to_char(len(game.events) - 1)}')
            return
        entry_order.extend(board)

    game.set_player(str(ctx.author.id), entry_order)
    global progress_embed
    progress_embed = None
    await ctx.message.add_reaction(SUCCESS_EMOJI)
    save_game_to_file()


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
    new_winners = game.hit(event.index)
    global progress_embed
    progress_embed = None
    embed = discord.Embed(
        title=embed_title('HIT', HIT_EMOJI),
        description=f'Event {index_to_emoji(event.index)}: "{event.desc}"'
    )
    await ctx.send(embed=embed)
    for winner_id in new_winners:
        board_str, mask_str = get_player_progress(winner_id)
        embed = discord.Embed(
            title=embed_title('WIN', '🎊 🥳 🎉 🎊 🥳 🎉'),
            description=f'<@{winner_id}> has just won!\n\n> {board_str}\n> {mask_str}'
        )
        await ctx.send(embed=embed)
    save_game_to_file()


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
    global progress_embed
    progress_embed = None
    embed = discord.Embed(
        title=embed_title('UNHIT', UNHIT_EMOJI),
        description=f'Event {index_to_emoji(event.index)}: "{event.desc}"'
    )
    await ctx.send(embed=embed)
    save_game_to_file()

'''
