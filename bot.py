from decouple import config
import json
import os
import pandas
import random

import discord
from discord.ext import commands

from check import *
from generate import generate
from inputparser import *

TOKEN = config('DISCORD_TOKEN')
ADMINS = ['mzhao#1429']

####################

state = dict()
inverse_state = dict()

lines = []
df = None

been_hit = [False] * 25

users_won = dict()

async def print_usage(ctx, command):
    await ctx.send(':cry: : <>%s [seed between 1-20]' % (command))

def matrix_to_strings(matrix):
    strings = []
    output_string = ''
    for row in matrix:
        output_string += ''.join(row) + '\n'
        if len(output_string) > 1000:
            strings.append(output_string)
            output_string = ''
    strings.append(output_string)
    return strings

async def print_grid(ctx, grid):
    strings = matrix_to_strings(grid)

    for s in strings:
        await ctx.send('```\n' + s + '\n```')

async def print_grid_from_seed(ctx, seed):
    grid = generate(seed).get_grid()
    await print_grid(ctx, grid)

async def check_user(ctx, user, do_print):
    if user not in state:
        await ctx.send(':cry: : You do not have a bingo board assigned')
        return

    grid, has_won = is_win(state[user])
    if do_print:
        if has_won:
            await ctx.send(':+1: : You have won!')
        else:
            await ctx.send(':-1: : You have not won yet!')
    await print_grid(ctx, grid.get_grid())

####################

bot = commands.Bot(command_prefix='<>')

@bot.event
async def on_ready():
    global state
    global parser
    global lines
    global df
    global been_hit
    print('Bot ready')
    with open('state.json', 'r') as file:
        state = json.load(file)
    parser = InputParser('lines.csv')
    lines = parser.get_lines()
    df = pandas.read_csv('lines.csv')
    for i in range(25):
        if df['did_occur'].at[i] == 'y':
            been_hit[i] = True
    for key, value in state.items():
        inverse_state[value] = key
    
    for user in state:
        users_won[user] = is_win(state[user])[1]

    print(state)

@bot.command(name='test')
async def test_command(ctx):
    await ctx.send('hello')

@bot.command(name='viewseed')
async def viewseed_command(ctx, arg):
    if str(ctx.author) not in ADMINS:
        await ctx.send(':cry: : You do not have permission to use this command')
        return
    try:
        seed = int(arg)
    except ValueError:
        await print_usage(ctx, 'viewseed')
        return
    if seed < 1 or seed > 20:
        await print_usage(ctx, 'viewseed')
        return
    
    await print_grid_from_seed(ctx, seed)

@bot.command(name='view')
async def view_command(ctx):
    user = str(ctx.author)
    if user not in state:
        await ctx.send(':cry: : You do not currently have a bingo board assigned. Use "<>select" to assign a board')
        return
    
    await ctx.send('You have previously selected seed = ' + str(state[user]))
    await print_grid_from_seed(ctx, state[user])

@bot.command(name='select')
async def select_command(ctx, *, arg):
    user = str(ctx.author)

    if user in state:
        await ctx.send(':cry: : You already have a bingo board assigned. Use "<>view" to view your assigned board')
        return
    
    if not arg:
        await print_usage(ctx, 'select')
        return

    try:
        seed = int(arg)
    except ValueError:
        await print_usage(ctx, 'select')
        return

    if seed < 1 or seed > 20:
        await print_usage(ctx, 'select')
        return
    
    if seed in inverse_state:
        await ctx.send(':cry: : ' + str(inverse_state[seed]) + ' has already selected that seed')
        return
    
    state[user] = seed
    inverse_state[seed] = user
    users_won[user] = is_win(seed)[1]
    with open('state.json', 'w') as file:
        json.dump(state, file)

    await ctx.send(str(ctx.author) + ' has selected seed = ' + str(seed) + '!')
    await print_grid_from_seed(ctx, state[user])

@bot.command(name='hit')
async def hit_command(ctx, *args):
    phrase = ' '.join(args)
    print('hit ' + phrase)

    matches = 0
    row_num = -1
    for r, line in enumerate(lines):
        if phrase in line:
            row_num = r
            matches += 1
    
    if matches == 0:
        await ctx.send(':cry: : "' + phrase + '" is not found in any line')
        return
    if matches > 1:
        await ctx.send(':cry: : "' + phrase + '" is found in multiple lines')
        return
    
    if been_hit[row_num]:
        await ctx.send(':cry: : "' + lines[row_num] + '" has already been hit')
        return

    been_hit[row_num] = True
    df['did_occur'].at[row_num] = 'y'
    df.to_csv('lines.csv', index=False)

    just_won = []
    for user in state:
        won = is_win(state[user])[1]
        if won and not users_won[user]:
            just_won.append(user)
            users_won[user] = True
    
    await ctx.send(':white_check_mark: : The line "' + lines[row_num] + '" has been hit!')

    for user in just_won:
        await ctx.send(':partying_face: : ' + user + ' has just won!')

@bot.command(name='unhit')
async def unhit_command(ctx, *args):
    phrase = ' '.join(args)
    print('unhit ' + phrase)

    matches = 0
    row_num = -1
    for r, line in enumerate(lines):
        if phrase in line:
            row_num = r
            matches += 1
    
    if matches == 0:
        await ctx.send(':cry: : "' + phrase + '" is not found in any line')
        return
    if matches > 1:
        await ctx.send(':cry: : "' + phrase + '" is found in multiple lines')
        return
    
    if not been_hit[row_num]:
        await ctx.send(':cry: : "' + lines[row_num] + '" was never hit')
        return
    
    been_hit[row_num] = False
    df['did_occur'].at[row_num] = 'n'
    df.to_csv('lines.csv', index=False)

    for user in state:
        users_won[user] = is_win(state[user])[1]

    await ctx.send(':x: : The line "' + lines[row_num] + '" has been unhit!')

@bot.command(name='unhitall')
async def unhitall_command(ctx):
    if str(ctx.author) not in ADMINS:
        await ctx.send(':cry: : You do not have permission to use this command')
        return
    for i in range(25):
        been_hit[i] = False
        df['did_occur'].at[i] = 'n'
    
    df.to_csv('lines.csv', index=False)

    await ctx.send(':x: : All lines have been unhit!')

@bot.command(name='lines')
async def lines_command(ctx):
    output_string = 'Here are all the lines:'
    for r, line in enumerate(lines):
        if been_hit[r]:
            output_string += '\n:white_check_mark: : '
        else:
            output_string += '\n:x: : '
        output_string += line
    await ctx.send(output_string)

@bot.command(name='check')
async def check_command(ctx):
    user = str(ctx.author)
    await check_user(ctx, user, True)

@bot.command(name='checkall')
async def checkall_command(ctx):
    for user in state:
        await ctx.send(user)
        await check_user(ctx, user, False)

@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await bot.close()
    print(state)
    print(inverse_state)
    with open('state.json', 'w') as file:
        json.dump(state, file)
    print("Bot Closed")

bot.run(TOKEN)