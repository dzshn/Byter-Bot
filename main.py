#!/usr/bin/env python3
import asyncio
import json
import os
import traceback
from sys import exc_info
from secrets import choice
from time import time
from urllib.parse import quote_plus

import discord
import requests

from src.commands import command_parser
from src.utils import utils, statushandler, emailhandler
from src.subbot import subbot

client = discord.Client(intents=discord.Intents(guild_messages=True, guilds=True))

client.initTime = time()
client.readyTime = 0
client.loadTime = 0
client.reDb = {}
client.ball8 = {}
client.jsonfiles = {i: json.load(open(json.load(open('data/index.json'))[i])) for i in json.load(open('data/index.json'))}
client.version = open('VERSION').read()

@client.event
async def on_ready():
    client.readyTime = time()
    async for i in client.get_channel(740539699134857337).history():
        if i.content in client.reDb:
            client.reDb[i.content].append(i.attachments[0].url)

        else:
            client.reDb[i.content] = [i.attachments[0].url]

    async for i in client.get_channel(742479941504860341).history():
        client.ball8[i.content] = i.attachments[0].url

    asyncio.create_task(emailhandler.start(client.get_channel(754876413043146823)), name="emailhandler")
    asyncio.create_task(statushandler.start(client), name="statushandler")
    #asyncio.create_task(subbot.run(), name="subbot")

    client.loadTime = time()

@client.event
async def on_message(m):
    if m.webhook_id == 740524198165872711 and client.user.id == 740006457805635678:
        await utils.bot_reload(client)

    if m.author.bot:
        return

    if m.channel.id == 740078363191935079 and client.user.id == 740006457805635678:
        return

    elif m.content.startswith(('%', 'b!')):
        try:
            await command_parser.parse_command(m, client)

        except:
            await m.channel.send(
                embed=discord.Embed(
                    color=0xfa0505, 
                    title='An unknown error ocurred',
                    description='this error has been anonimously reported to my dev, if possible please open a issue [on my server](https://discord.gg/h4sFrNj)'
            ))

            raise Exception("Unknown error on command")


    elif m.channel.id == 740539699134857337:
        if m.content in client.reDb:
            client.reDb[m.content].append(m.attachments[0].url)

        else:
            client.reDb[m.content] = [m.attachments[0].url]

@client.event
async def on_error(func, *args, **kwargs):
    embed = discord.Embed(
        color=0xfa0505, 
        title="**Error!**",
        description="\n\n**Exception info:**\n"          +
                    "**Type :** %s\n"  % exc_info()[0] + 
                    "**Value :** %s\n" % exc_info()[1] +
                    "**Traceback :**\n"                  +
                    "```py\n%s\n```"     % traceback.format_exc()
    )

    if func == "on_message":
        embed.description = "**Message content :** %s" % args[0].content + embed.description

    else:
        embed.description = "**Function :** %s\n\n**Args :** %s\n\n**Kwargs :** %s\n" % (func, args, kwargs) +embed.description

    await client.get_channel(741024906774577201).send(client.get_user(310449948011528192).mention, embed=embed)

client.run(open('TOKEN').read())