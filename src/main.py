from decouple import config

from bot.bot import bot

TOKEN = config('DISCORD_TOKEN')
bot.run(TOKEN)