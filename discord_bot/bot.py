import aiohttp
from discord.ext import commands
import discord

import aiohttp
import asyncio

with open(".token") as f:
    token = f.read()

async def get_profanity(msg: str):
    async with aiohttp.ClientSession() as session:
        params = {"sent": msg}
        async with session.get(r'http://ec2-13-212-167-131.ap-southeast-1.compute.amazonaws.com/api', params=params) as response:

            print(response.url)
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            json_output = await response.json()
            print(json_output)

        return json_output['profanity']

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return
    print("recvd")
    if msg.content:
        toxic = False

        profanity_rating = await get_profanity(msg.content)
        toxic = profanity_rating > 0.7
        if toxic:
            print("deleted")
            await msg.author.send(f'The message: "{msg.content}" you sent in channel {msg.channel} was not appropriate. The message has been deleted')
            await msg.delete()

bot.run(token)