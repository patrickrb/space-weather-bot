import discord
import aiohttp
import asyncio

# User configuration
bot_token = 'MTEwMDc3OTY3NTU2MDcxNDI1MQ.GYOSXD.1zbYxRenmD6V5Lk2QGnChtFOvkcUegmOOp-qvE'
bot_username = 'space-weather'
avatar_url = 'https://storage.googleapis.com/gn-static-production-assets/champs/36/phase_headshot_2s/mcpufferson-headshot-2.3x_1521144067.png'

# URL of the text file to fetch
url = 'https://services.swpc.noaa.gov/text/3-day-forecast.txt'

# Channel ID where the bot will post the message
channel_id = 1100773269050757161

# Interval for checking the website (in seconds)
interval = 86400 # 24 hours

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
    await channel.send(message)

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
            await post_message(channel, text)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f'Error: {e}')
            await asyncio.sleep(interval)

# Start the bot client and check the website
@bot.event
async def on_ready():
    print('Bot is ready.')
    await update_bot_profile()
    bot.loop.create_task(check_website())

# Run the bot client
bot.run(bot_token)
