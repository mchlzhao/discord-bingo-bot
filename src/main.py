from decouple import config

from bot.bot import bot
from bot.embed import embed_command

TOKEN = config('DISCORD_TOKEN')
bot.run(TOKEN)