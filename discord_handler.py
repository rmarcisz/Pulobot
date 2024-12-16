import discord
import pulobot
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    scenario_images = []
    if message.content[:5] == '!pule':
        files = pulobot.get_pule(str(message.content[5:]))
        for file in files:
            scenario_images.append(discord.File(file))
        await message.channel.send(files=scenario_images)

bot.run(DISCORD_TOKEN)