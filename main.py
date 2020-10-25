#!/usr/bin/env python3
import asyncio
import hashlib
import json
import traceback
from sys import exc_info
from time import time
from urllib.parse import quote_plus

import discord
import requests

from src.commands import command_parser
from src.utils import utils, statushandler, emailhandler

client = discord.Client(intents=discord.Intents(guild_messages=True, guilds=True))

client.initTime = time()
client.main_script_hash = hashlib.sha512(open("./main.py").read().encode()).hexdigest()
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
            await utils.handle_error(client, message=m)

    elif m.channel.id == 740539699134857337:
        if m.content in client.reDb:
            client.reDb[m.content].append(m.attachments[0].url)

        else:
            client.reDb[m.content] = [m.attachments[0].url]

    elif m.channel in client.get_channel(741765710971142175).channels and m.channel.id != 745400744303394917:
        data = requests.get('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='+quote_plus(m.clean_content)).content.decode()
        embed = discord.Embed(
            color=0x301baa,
            title=f"from channel {m.channel.name}",
            description=(
                f"**message content:** {m.content}\n"
                f"**from:** {m.author.name}\n"
                f"**translation:** {json.loads(data)[0][0][0]}"
            )
        )
        embed.set_footer(text="Powered by Google Translate")
        await client.get_channel(745400744303394917).send(embed=embed)

    elif client.get_user(310449948011528192) in m.mentions and not m.author.bot:
        await m.add_reaction(client.get_emoji(748824813501546559))

    if m.guild == client.get_guild(725421276562325514):
        if "good night" in m.content.lower() or "goodnight" in m.content.lower():
            await m.add_reaction("❤️")

        elif "dreamworks" in m.content.lower():
            await m.add_reaction(client.get_emoji(726611950200553502))


@client.event
async def on_error(func, *args, **kwargs):
    out_tb, att = utils.clean_tb()
    await client.get_channel(741024906774577201).send(
        client.get_user(310449948011528192).mention,
        embed=discord.Embed(
            color=0xfa0505,
            title="**Error!**",
            description=(
                "**Error not made within a command? uh oh~**\n"
                "**Full data found is as following**\n\n"
                f"**func :** {func}"
                f"**args :** {args}"
                f"**kwargs :** {kwargs}"
                f"**exc_info :** {exc_info()}"
                "**Traceback :**"
                f"```py{out_tb}```"
            )
        ),
        file=att
    )


client.run(open('TOKEN').read())
