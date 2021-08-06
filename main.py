from decouple import config
from discord.ext import commands

from src.bot.game_management_cog import GameManagementCog
from src.bot.event_hitting_cog import EventHittingCog
from src.core.game_engine import GameEngine
from src.repos.in_memory.data_store import DataStore
from src.repos.in_memory.in_memory_event_repo import InMemoryEventRepo
from src.repos.in_memory.in_memory_game_repo import InMemoryGameRepo
from src.repos.in_memory.in_memory_player_repo import InMemoryPlayerRepo

data_store = DataStore()
event_repo = InMemoryEventRepo(data_store)
game_repo = InMemoryGameRepo(data_store)
player_repo = InMemoryPlayerRepo(data_store)
engine = GameEngine(event_repo, game_repo, player_repo)

bot = commands.Bot(command_prefix='<>', help_command=None)
bot.add_cog(GameManagementCog(bot, engine))
bot.add_cog(EventHittingCog(bot, engine))

TOKEN = config('DISCORD_TOKEN')
bot.run(TOKEN)
