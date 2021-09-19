import os

import psycopg2
from discord.ext import commands

from src.bot.event_hitting_cog import EventHittingCog
from src.bot.game_management_cog import GameManagementCog
from src.bot.player_control_cog import PlayerControlCog
from src.bot.view_game_cog import ViewGameCog
from src.core.game_engine import GameEngine
from src.repos.in_memory.data_store import DataStore
from src.repos.in_memory.in_memory_event_repo import InMemoryEventRepo
from src.repos.in_memory.in_memory_game_repo import InMemoryGameRepo
from src.repos.in_memory.in_memory_player_repo import InMemoryPlayerRepo
from src.repos.postgres.postgres_event_repo import PostgresEventRepo
from src.repos.postgres.postgres_game_repo import PostgresGameRepo
from src.repos.postgres.postgres_player_repo import PostgresPlayerRepo

USE_IN_MEMORY = False

if USE_IN_MEMORY:
    data_store = DataStore()
    event_repo = InMemoryEventRepo(data_store)
    game_repo = InMemoryGameRepo(data_store)
    player_repo = InMemoryPlayerRepo(data_store)
else:
    DATABASE_URL = os.environ['DATABASE_URL']
    sslmode = 'require' if 'HEROKU' in os.environ else 'disable'
    conn = psycopg2.connect(DATABASE_URL, sslmode=sslmode)
    event_repo = PostgresEventRepo(conn)
    game_repo = PostgresGameRepo(conn)
    player_repo = PostgresPlayerRepo(conn)

engine = GameEngine(event_repo, game_repo, player_repo)

bot = commands.Bot(command_prefix='<>', help_command=None)
bot.add_cog(EventHittingCog(bot, engine))
bot.add_cog(GameManagementCog(bot, engine))
bot.add_cog(PlayerControlCog(bot, engine))
bot.add_cog(ViewGameCog(bot, engine))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.reply(
            "Command not found. Use <>help to view info on all commands.")


TOKEN = os.environ['DISCORD_TOKEN']
bot.run(TOKEN)
