import hashlib
import asyncio
import json
import os
import traceback
from io import BytesIO
from sys import exc_info

import discord

from . import errors

def clean_tb():
    out = traceback.format_exc()
    out.replace("`", "'")
    att = None
    if len(out) > 1750:
        att = discord.File(BytesIO(out_tb.encode()), filename="traceback.txt")
        out_tb = out_tb[:1750] + '\n[...]\n**SHORTENED :** Full output at attatchment'

    return clean_tb, att

async def bot_reload(c, update=True, delay=True, force_execl=False):
    if delay:
        for i in asyncio.all_tasks():
            if i.get_name() == "statushandler":
                i.cancel()

        await c.change_presence(activity=discord.Game("Update incoming! Rebooting in a minute!"))
        await asyncio.sleep(55)
        await c.change_presence(activity=discord.Game("Updating and rebooting..."))
        await asyncio.sleep(5)
        await c.close()

    if update:
        os.system("git pull")

    if c.main_script_hash != hashlib.sha512(open("./main.py").read().encode()).hexdigest() or force_execl:
        os.execl("./main.py", "main")

async def handle_error(c, message):
    exception = exc_info()[1]
    if isinstance(exception, errors.CommandError):
        await message.channel.send(
            embed=discord.Embed(
                color=0xfa0505,
                title='An error ocurred',
                description='Error is %s' % exception
        ))

    else:
        await message.channel.send(
            embed=discord.Embed(
                color=0xfa0505, 
                title='An unknown error ocurred',
                description='this error has been anonimously reported to my dev, if possible please open a issue [on my server](https://discord.gg/h4sFrNj)'
        ))

        out_tb, att = clean_tb()

        await c.get_channel(741024906774577201).send(
            c.get_user(310449948011528192).mention,
            embed=discord.Embed(
                color=0xfa0505,
                title="**Error!**",
                description=f'''**Message content :** {message.content}

                                **Exception info:**
                                **Value :** {exception}
                                **Traceback :**
                                ```py
                                {traceback.format_exc()}
                                ```'''
            ),
            file=att
        )
