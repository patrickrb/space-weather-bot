import os
from io import BytesIO
from PIL import Image
from datetime import datetime

import discord
import aiohttp
import asyncio

# User configuration
bot_token = os.environ.get('DISCORD_BOT_TOKEN')
bot_username = 'space-weather'
avatar_url = 'https://storage.googleapis.com/gn-static-production-assets/champs/36/phase_headshot_2s/mcpufferson-headshot-2.3x_1521144067.png'

# URL of the text file to fetch
url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'

# Channel ID where the bot will post the message
channel_id = int(os.environ.get('DISCORD_CHANNEL_ID'))

# Interval for checking the website (in seconds)
interval = int(os.environ.get('DISCORD_POST_INTERVAL'))

# Enable privileged intents for the bot
intents = discord.Intents.default()
intents.members = True

# Initialize the bot client
bot = discord.Client(intents=intents)

# Fetch the text file from the website
async def get_forecast():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return text.strip()

# Post the message to the specified channel
async def post_message(channel, message):
    embed = discord.Embed(title='Weather for ' + datetime.today().strftime('%m/%d/%Y'), description=message, color=0x00ff00)
    await channel.send(embed=embed)

# Update the bot's username and avatar
async def update_bot_profile():
    await bot.wait_until_ready()
    await bot.user.edit(username=bot_username, avatar=await get_avatar())

# Fetch the avatar image from the specified URL
async def get_avatar():
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            data = await response.read()
            return data

# Check the website and post the message to the specified channel
async def check_website():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    while not bot.is_closed():
        try:
            text = await get_forecast()
            image = await get_image_data('https://www.hamqsl.com/solarn0nbh.php')
            await post_message(channel, text)
            await post_image(channel, image)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f'Error: {e}')
            await asyncio.sleep(interval)

async def post_image(channel, img_data):
        # create an Image object from the raw data
        img = Image.open(BytesIO(img_data))

        # create a BytesIO object to hold the image data
        img_buffer = BytesIO()
        img = img.convert('RGB')
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)

        # send the image to the channel
        await channel.send(file=discord.File(fp=img_buffer, filename='image.jpg'))

async def get_image_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img_bytes = await response.read()

    return img_bytes
    
# Start the bot client and check the website
@bot.event
async def on_ready():
    print('Bot is ready.')
    # Uncomment the line below to update the bot's username and avatar
    # Discord was kicking me out because I was changing the profile too often
    # await update_bot_profile()
    bot.loop.create_task(check_website())

# Run the bot client
bot.run(bot_token)
