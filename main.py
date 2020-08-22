#!/usr/bin/env python3

from urllib.parse import quote_plus
from datetime import timedelta
from asyncio import sleep
from random import choice
from sys import exc_info
from time import time
from sys import argv
from re import sub
import requests
import discord
import json
import os

initTime = time()

devmode = len(argv) != 1 and argv[1] == "dev"
if devmode:
    tkn = "NzQzMzAyMTQ3OTI3NDQxNDU5.XzSsEQ.yWp07ZSoOIhoIFm7oTE9ROuUrs4"
else:
    tkn = "NzQwMDA2NDU3ODA1NjM1Njc4.XyiuuA.O2PFUXd4r-GZVfw-g5CZVHMQacc"

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
        if m.content.startswith(('%', 'b!')):
            ctx = m.content[1:].split(' ') if m.content.startswith('%') else m.content[2:].split(' ')
            cm = ctx[0]

            if cm == "embed":
                await m.channel.send('', embed=discord.Embed.from_dict(json.loads(m.content.split('embed')[1])))
                await m.delete()

            elif cm == "gifs":
                embed = discord.Embed(color=0x301baa,
                                      title="Hey, there are %s categories loaded" % len(self.reDb),
                                      description='''
**categories:** %s

you may use the categories as a command, and I'll pick an image/gif from there!
                                      ''' % str(self.reDb.keys())[10:].strip("()[]").replace("'", '')
                )
                await m.channel.send('', embed=embed)

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
                await m.channel.send('', embed=embed)

            elif cm == "info":
                if len(ctx) == 1:
                    embed = discord.Embed(color=0x301baa,
                                          title="**Info!**",
                                          description='''
Currently there's info only for characters!
use `char` or `character` after this command to see it!
                                                ''')
                    embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                    embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                     icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")

                elif ctx[1] in ["character", "char"]:
                    if len(ctx) == 2:
                        embed = discord.Embed(color=0x00002a,
                                              title="**Characters!**",
                                              description='''
Want to know about the créu characters? this is the way to go!

Just put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course me!
                                              '''
                                            )
                        embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                        embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                         icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                        await m.channel.send('', embed=embed)
                    if ctx[2].lower().replace('&','').replace('é','e') in self.jsonfiles['char']:
                        return 1

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

                await m.channel.send('', embed=embed)

            elif cm == "t":
                if devmode:
                    await m.channel.send("```"+m.content+"```")
                    print(m.content)

                else:
                    await m.channel.send('Bot online', delete_after=5)
                    await m.delete()


            elif cm == "poll":
                await m.delete()
                embed = discord.Embed(color=0x301baa)
                options = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷' ,'🇸', '🇹']
                poll = m.content.replace('b!', '%')[5:].split(',')
                if len(ctx) == 1:
                    poll[0] = 'poll'
                pollText = ''
                for i in poll[1:]:
                    pollText += options[poll[1:].index(i)]+' '+i+'\n'
                if len(poll) == 1:
                    pollText = '✅ / ❎'
                embed.add_field(name=poll[0].strip().title(),
                                value=pollText)
                pollMsg = await m.channel.send('', embed=embed)
                for i in range(len(poll[1:])):
                    await pollMsg.add_reaction(options[i])
                if len(poll) == 1:
                    await pollMsg.add_reaction('✅')
                    await pollMsg.add_reaction('❎')

            elif cm == "stats":
                embed = discord.Embed(color=0x301baa)
                embed.add_field(name="Here are some numbers I found",
                                value='''
**uptime**: I'm online for %s (%s seconds)
**ready time**: I took %s seconds to connect to discord
**loading time**: I took %s seconds to load after connecting
                                      '''
                                      % (
                                         timedelta(seconds=round(time()-initTime)),
                                         round(time()-initTime, 2),
                                         round(self.readyTime-initTime, 2),
                                         round(self.loadTime-self.readyTime, 2)
                                        ),
                                inline=False)
                embed.set_footer(text="version %s - bot made by leninnog" % self.version)
                await m.channel.send('', embed=embed)

            elif cm == "time":
                if len(ctx) == 1:
                    embed = discord.Embed(title="Timezones!",
                                          description='''
timezones can be weird some times, but hopefully there's an api I can push data from!

The avaiable areas are: Africa, America, Antartica, Asia, Atlantic, Australia, CET, CST6CDT, EET, EET5EDT, Etc, Europe, HST, Indian, MET, MST, MST5MDT, PST8PDT, Pacific and WET
                                          ''')

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
                await m.channel.send('', embed=embed)

            elif cm == "tos":
                if m.author.id == 310449948011528192:
                    await m.channel.send('', embed=discord.Embed.from_dict(self.jsonfiles['tos']['welcome']))
                    await m.channel.send('', embed=discord.Embed.from_dict(self.jsonfiles['tos']['section1']))
                    await m.channel.send('', embed=discord.Embed.from_dict(self.jsonfiles['tos']['section2']))
                    await m.channel.send('', embed=discord.Embed.from_dict(self.jsonfiles['tos']['section3']))

                    await m.delete()

                else:
                    await m.channel.send('tos: acess denied!')

            elif cm == "8ball":
                sball8 = choice(list(self.ball8))
                if len(cm) == 1:
                    title = "**"+sball8+"**"
                    desc=""

                else:
                    title = m.content.replace('b!', '%')[6:]
                    desc = sball8

                embed = discord.Embed(color=0x2031ba,
                                      title=title,
                                      description=desc
                                     )
                embed.set_image(url=self.ball8[sball8])
                embed.set_footer(text="8ball by zuli - bot by leninnog")
                await m.channel.send('', embed=embed)

            elif cm in self.reDb:
                await m.channel.send(choice(self.reDb[cm]))

            else:
                await m.channel.send(cm + ': command not found')

        elif m.webhook_id == 740524198165872711:
            await self.close()
            if devmode:
                args = "dev"
            
            else:
                args = ""

            os.system("git pull")
            os.execl("./main.py", args)

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]

        elif m.channel.category != None and m.channel.category.id == 741765710971142175 and m.channel.id != 745400744303394917:
            data = requests.get('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='+quote_plus(sub(r'[\!?/&]', ' ', m.clean_content))).content.decode()
            embed = discord.Embed(color=0x301baa,
                                  title="from channel"+m.channel.name,
                                  description="**message content:** %s\n**from:** %s\n**translation:** %s" % (
                                    m.clean_content, m.author.name, json.loads(data)[0][0][0]
                                  )
            )
            embed.set_footer(text="Powered by Google Translator")            

        elif m.content.lower().replace(',', '').startswith("wait, it's all ") and m.content.endswith('?'):
            async with m.channel.typing():
                await sleep(2)
            await m.channel.send('always has been')
            async with m.channel.typing():
                await sleep (3)
            await m.channel.send("I'm sorry "+m.author.name)

        elif ("good night" in m.content.lower() or "goodnight" in m.content.lower()) and m.guild.id == 725421276562325514:
            await m.add_reaction("❤️")

        elif "dreamworks" in m.content.lower() and m.guild.id == 725421276562325514:
            await m.add_reaction(self.get_emoji(726611950200553502))

    async def on_error(self, error, *args, **kwargs):
        await self.get_guild(740069078735257672).get_channel(741024906774577201).send(
            self.get_user(310449948011528192).mention, embed=discord.Embed.from_dict(
                {
                    "color": 0xfa0505,
                    "title": "**Error!**",
                    "description": "**at function:** %s\n\n**with args:** %s\n\n**with kwargs:** %s\n\n**traceback:** %s" % (error, args, kwargs, exc_info())
                }
            )
        )

bot = byterbot()
bot.run(tkn)