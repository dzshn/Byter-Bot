import discord
from asyncio import sleep

async def start(bot):
    while True:
        await bot.change_presence(
            activity=discord.Game(
                "at "+str(len(bot.guilds))+" servers! My prefix is b! or %"
            )
        )
        await sleep(60)