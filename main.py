#!/usr/bin/env python3

from urllib.parse import quote_plus
from datetime import timedelta
from random import choice
from sys import exc_info
from time import time
from re import sub
import traceback
import requests
import asyncio
import aiohttp
import discord
import psutil
import json
import os

initTime = time()

tkn = open("TOKEN").read()

class byterbot(discord.Client):
    reDb = {}
    ball8 = {}

    readyTime = 0
    loadTime = 0

    dataindex = open('data/index.json')
    dataindex = json.load(dataindex)
    jsonfiles = {}

    version = open('VERSION').read()

    for i in dataindex:
        jsonfiles.update({i:json.load(open(dataindex[i]))})

    async def on_ready(self):
        self.readyTime = time()
        async for i in self.get_channel(740539699134857337).history():
            if i.content in self.reDb:
                self.reDb[i.content].append(i.attachments[0].url)

            else:
                self.reDb[i.content] = [i.attachments[0].url]

        async for i in self.get_channel(742479941504860341).history():
            self.ball8[i.content] = i.attachments[0].url

        self.loadTime = time()

    async def on_message(self, m):
        if m.author.bot and m.webhook_id != 740524198165872711:
            return 1

        if m.channel.id == 740078363191935079 and self.user == await self.get_user(740006457805635678):
            return 1

        elif m.content.startswith(('%', 'b!')):
            ctx = m.content[1:].split(' ') if m.content.startswith('%') else m.content[2:].split(' ')
            cm = ctx[0]

            if cm == "embed":
                if m.channel.type == discord.ChannelType.text and not m.author.permissions_in(m.channel).manage_messages:
                    await m.channel.send('Missing permissions! you need manage messages to do that')
                    return 1

                if len(ctx) == 1:
                    await m.channel.send(
                        embed=discord.Embed(
                            color=0x301baa,
                            title="Embeds!",
                            description='''
You can use this command using the standard json format, without the outer brackets, example:

%embed "title": "Title here", "description": "Description here"

for reference, the valid keywords can be seen [here](https://discord.com/developers/docs/resources/channel#embed-object-embed-structure) and you can check it on [this visualizer](https://leovoel.github.io/embed-visualizer/)
                            '''
                        )
                    )

                else:
                    try:
                        await m.channel.send(embed=discord.Embed.from_dict(json.loads("{%s}" % m.content[6:])))
                    except json.JSONDecodeError:
                        await m.channel.send('There was an error parsing your data', delete_after=5)

                    await m.delete()

            elif cm == "gifs":
                await m.channel.send(
                    embed=discord.Embed(
                        color=0x301baa,
                        title="Hey, there are %s categories loaded" % len(self.reDb),
                        description='''
**categories:** %s

you may use the categories as a command, and I'll pick an image/gif from there!
                        ''' % str(self.reDb.keys())[10:].strip("()[]").replace("'", '')
                    )
                )

            elif cm == "help":
                if len(ctx) == 1:
                    data = self.jsonfiles['help']['index']

                else:
                    if ctx[1] in self.jsonfiles['help']:
                        data = self.jsonfiles['help'][ctx[1]]

                    else:
                        await m.channel.send('help: %s: page not found' % ctx[1])
                        return 1

                embed = discord.Embed(color=0x301baa, title=data['title'], description=''.join(data['description']))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/741457274530299954/741457798705184830/BUTTON_byter.webp")
                embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                 icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                await m.channel.send(embed=embed)

            elif cm == "info":
                if len(ctx) == 1:
                    embed = discord.Embed(
                        color=0x301baa,
                        title="**Info!**",
                        description='''Currently there's info only for characters!
use `char` or `character` after this command to see it!'''
                    )

                    embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                    embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                     icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")

                elif ctx[1] in ["character", "char"]:
                    if len(ctx) == 2:
                        embed = discord.Embed(
                            color=0x00002a,
                            title="**Characters!**",
                            description='''
Want to know about the créu characters? this is the way to go!

Just put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course, me!
                            '''
                        )

                        embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                        embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                         icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                        await m.channel.send(embed=embed)
                        return 1

                    elif ctx[2].lower().replace('&','').replace('é','e') in self.jsonfiles['char']:
                        charData = self.jsonfiles['char'][ctx[2].lower().replace('&','').replace('é','e')]

                    else:
                        charData = {
                            "color": "0xD3D152",
                            "thumb": "https://cdn.discordapp.com/attachments/741457274530299954/741553915740422204/thonk.png",
                            "name": "%s: Not found\n" % ctx[2],
                            "desc": "???",
                            "favs": ["???","???","???"],
                            "img": "https://cdn.discordapp.com/attachments/741457274530299954/741553915740422204/thonk.png"
                        }

                    embed = discord.Embed(color=int(charData['color'], 16))
                    embed.set_thumbnail(url=charData['thumb'])
                    embed.add_field(name=charData['name'], value=charData['desc'], inline=False)
                    embed.add_field(name="Favorites", value="<:coffee:741469635492446268> %s\n\n<:ice_cream:741469513773613118> %s\n\n<:music:741469877143076946> %s" % tuple(charData['favs']), inline=False)
                    embed.set_image(url=charData['img'])
                    embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                     icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")

                await m.channel.send(embed=embed)

            elif cm == "t":
                await m.channel.send('Bot online', delete_after=5)
                await m.delete()

            elif cm == "poll":
                options = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷' ,'🇸', '🇹']
                poll = m.content.replace('b!', '%')[5:].split(',')
                pollText = ''
                for i in poll[1:]:
                    pollText += options[poll[1:].index(i)]+' '+i+'\n'

                if len(poll) == 1:
                    pollText = '✅ / ❎'

                pollMsg = await m.channel.send(
                    embed=discord.Embed(
                        color=0x301baa,
                        title=poll[0].strip(),
                        description=pollText
                    )
                )
                for i in range(len(poll[1:])):
                    await pollMsg.add_reaction(options[i])

                if len(poll) == 1:
                    await pollMsg.add_reaction('✅')
                    await pollMsg.add_reaction('❎')

                await m.delete()

            elif cm == "stats":
                embed = discord.Embed(
                    color=0x301baa,
                    title="**Here are some numbers I found**"
                )

                embed.add_field(
                    name="**Time Metrics:**",
                    value='''
**Uptime :** %s (%s seconds)
**Time since last disconnect: ** %s (%s seconds)
**Connection load time :** %s
**Load time after connection :** %s
                    ''' % (
                        timedelta(seconds=round(time()-initTime)),
                        round(time()-initTime, 2),
                        timedelta(seconds=round(time()-self.readyTime)),
                        round(time()-self.readyTime, 2),
                        round(self.readyTime-initTime, 2),
                        round(self.loadTime-self.readyTime, 2)
                    )
                )

                embed.add_field(
                    name="**Usage data:**",
                    value='''
**Server Count :** %s
**CPU :** %s
**RAM :** %s
**Swap :** %s
                    ''' % (
                        len(self.guilds),
                        psutil.cpu_percent(),
                        psutil.virtual_memory().percent,
                        psutil.swap_memory().percent
                    )
                )

                embed.set_footer(text="version %s - bot made by leninnog" % self.version)
                await m.channel.send(embed=embed)

            elif cm == "time":
                if len(ctx) == 1:
                    embed = discord.Embed(
                        title="Timezones!",
                        description='''
Timezones can be weird some times, but hopefully there's an api I can push data from!

The avaiable areas are: Africa, America, Antartica, Asia, Atlantic, Australia, CET, CST6CDT, EET, EET5EDT, Etc, Europe, HST, Indian, MET, MST, MST5MDT, PST8PDT, Pacific and WET
                        '''
                    )

                else:
                    page = str(ctx[1:]).strip('[]').replace("'",'').replace(', ', '/')
                    data = requests.get('http://worldtimeapi.org/api/'+page).json()
                    data_out = ""
                    title = "**"+page+"**"

                    if "datetime" in data:
                        data_out = "**Current time:** %s\n**UTC offset:** %s" % (
                            data['datetime'].split('T')[1][:8], data['utc_offset']
                        )
                        title += "'s current time"

                    elif "error" in data:
                        data_out = data['error']
                        title += ": error!"

                    else:
                        for i in data:
                            i = i.lower().replace(ctx[1], '').lstrip('/')
                            data_out += i+', '
                        title += "'s avaiable timezones"

                    embed = discord.Embed(title=title, description=data_out)

                embed.set_footer(text="Powered by worldtimeapi.org - bot made by leninnog")
                await m.channel.send(embed=embed)

            elif cm == "8ball":
                ball8msg = None
                while True:
                    sball8 = choice(list(self.ball8))
                    embed = discord.Embed(
                        color=0x301baa,
                        title="**"+sball8+"**"
                    )

                    embed.set_image(url=self.ball8[sball8])
                    embed.set_footer(text="8ball by zuli - bot by leninnog")
                    if ball8msg == None:
                        ball8msg = await m.channel.send(embed=embed)

                    else:
                        await ball8msg.edit(embed=embed)

                    if not m.guild.me.permissions_in(m.channel).manage_messages:
                        return 1

                    await ball8msg.add_reaction("🔄")
                    def chk(r, u):
                        return str(r.emoji) == "🔄" and r.message.id == ball8msg.id and u == m.author

                    try:
                        r, u = await self.wait_for('reaction_add', check=chk, timeout=120)

                    except asyncio.TimeoutError:
                        return 1

                    await r.remove(u)

            elif cm in self.reDb:
                await m.channel.send(choice(self.reDb[cm]))

            else:
                await m.channel.send(cm + ': command not found')

        elif m.webhook_id == 740524198165872711:
            if self.user.id == 740006457805635678:
                await self.close()
                os.system("git pull")
                os.execl("./main.py", "")

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]

        elif m.channel in self.get_channel(741765710971142175).channels and m.channel.id != 745400744303394917:
            data = requests.get('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='+quote_plus(m.clean_content)).content.decode()
            embed = discord.Embed(
                color=0x301baa,
                title="from channel "+m.channel.name,
                description='''
**message content:** %s
**from:** %s
**translation:** %s"
                ''' % (
                    m.clean_content, m.author.name, json.loads(data)[0][0][0]
                )
            )

            embed.set_footer(text="Powered by Google Translator")

            await self.get_channel(745400744303394917).send(embed=embed)

        elif self.get_user(310449948011528192) in m.mentions and not m.author.bot:
            await m.add_reaction(self.get_emoji(748824813501546559))

        elif ("good night" in m.content.lower() or "goodnight" in m.content.lower()) and m.guild.id == 725421276562325514:
            await m.add_reaction("❤️")

        elif "dreamworks" in m.content.lower() and m.guild.id == 725421276562325514:
            await m.add_reaction(self.get_emoji(726611950200553502))

    async def on_error(self, func, *args, **kwargs):
        if exc_info()[1] == discord.Forbidden:
            return 1

        embed = discord.Embed(
            color=0xfa0505,
            title="**Error!**",
            description='''
**Exception info:**
**Type :** %s

**Value :** %s

**At line :** %s

**Traceback :**
```py
%s
```
            ''' % (exc_info()[0], exc_info()[1], exc_info()[2].tb_lineno, traceback.format_exc())
        )

        if func == "on_message":
            embed.description = "**Message content :** %s\n%s" % (args[0].content,embed.description)

        else:
            embed.description = "**Function :** %s\n\n**Args :** %s\n\n**Kwargs :** %s\n" % (func, args, kwargs, embed.description)

        await self.get_channel(741024906774577201).send(self.get_user(310449948011528192).mention, embed=embed)

bot = byterbot()
bot.run(tkn)