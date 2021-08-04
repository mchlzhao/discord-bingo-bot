from decouple import config

from src.bot.bot import bot

TOKEN = config('DISCORD_TOKEN')
bot.run(TOKEN)
