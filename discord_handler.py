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
        if pulobot.message_read(message.content[5:]) == 'error':
            await message.channel.send('Unrecognized input. Please format the message as !pule [number of rounds],[gg],[name],[options]. \n For more information please check https://wincyjneverbornow.blogspot.com/2024/12/pulobotmanual.html')
        else:
            files = pulobot.get_pule(str(message.content[6:]))
            for file in files:
                scenario_images.append(discord.File(file))
            await message.channel.send(files=scenario_images)

bot.run(DISCORD_TOKEN)