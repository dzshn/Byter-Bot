import asyncio
import json
import os

import discord


async def bot_reload(c, update=True):
    for i in asyncio.all_tasks():
        if i.get_name() == "statushandler":
            i.cancel()

    await c.change_presence(activity=discord.Game("Update incoming! Rebooting in a minute!"))
    await asyncio.sleep(55)
    await c.change_presence(activity=discord.Game("Updating and rebooting..."))
    await asyncio.sleep(5)
    await c.close()
    if update == True:
        os.system("git pull")

    os.execl("./main.py", "main")