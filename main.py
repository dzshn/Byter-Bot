from datetime import timedelta
from asyncio import sleep
from random import choice
from time import time
import discord
import json

initTime = time()

class byterbot(discord.Client):
    reDb = {}
    readyTime = 0
    loadTime = 0

    characters = open('data/characters.json')
    characters = json.load(characters)

    async def on_ready(self):
        self.readyTime = time() 
        
        async for i in self.get_channel(740539699134857337).history():
            if i.content in self.reDb:
                self.reDb[i.content].append(i.attachments[0].url)
            else:
                self.reDb[i.content] = [i.attachments[0].url]
        self.loadTime = time()

    async def on_message(self, m):
        if m.content.startswith(('%', 'b!')):
            ctx = m.content[1:].split(' ') if m.content.startswith('%') else m.content[2:].split(' ')
            cm = ctx[0]

            if cm == "help":
                embed=discord.Embed(color=0x301baa)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/741457274530299954/741457798705184830/BUTTON_byter.webp")
                embed.add_field(name="Hello! here are the valid commands",
                                value='''
                                        **help** - show this info about commands
                                        **info** - shows many infos about créu and his friends!
                                        **gifs** - lists all loaded categories of gifs/images
                                        **stats** - shows some useful stats
                                        **poll title, *options** - makes a poll, options may be none (yes/no) or phrases separated by a comma (up to 20), title may also be omitted if there arent other arguments
                                      ''',
                                inline=False)
                embed.add_field(name="And functions",
                                value='''
                                        **gifs / images !** - use the command %gifs to see what categories are avaiable and use % plus the name for me to pick a gif/image for you!
                                      ''',
                                inline=False)
                embed.add_field(name="Also, here is a copyright disclaimer!",
                                value='''
                                        © 2020 PriVer. All rights reserved. All visual content on this bot (including characters, images and trademarks) are protected by Intellectual Property rights owned by Priscila Vertamatti.
                                      ''',
                                inline=False)
                embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                 icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                await m.channel.send('', embed=embed)

            elif cm == "info":
                if ctx[1] in ["character", "char"]:
                    if len(ctx) == 2:
                        embed = discord.Embed(color=0x00002a)
                        embed.add_field(name="Characters!",
                                        value='''
                                                Want to know about the créu characters? this is the way to go!

                                                Just put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course me!
                                              ''',
                                        inline=False)
                        embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                        embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                         icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                        await m.channel.send('', embed=embed)
                        return 1

                    if ctx[2].lower().replace('&','').replace('é','e') in self.characters:
                        charData = self.characters[ctx[2].lower().replace('&','').replace('é','e')]

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
                await m.channel.send('Bot online')
                print(m.content)

            elif cm == "gifs":
                embed = discord.Embed(color=0x301baa)
                embed.add_field(name="Hey, there are %s categories loaded" % len(self.reDb),
                                value="**categories:** %s\n\nyou may use the categories as a command, and I'll pick an image/gif from there!" % str(self.reDb.keys())[10:].strip("()[]").replace("'", ''),
                                inline=False)
                await m.channel.send('', embed=embed)

            elif cm == "stats":
                embed = discord.Embed(color=0x301baa)
                embed.add_field(name="Here are some time metrics",
                                value='''
                                        **uptime**: I'm online for %s (%s seconds)
                                        **ready time**: I took %s seconds to connect to discord
                                        **load time**: I took %s seconds to load after connecting
                                      '''
                                      % (
                                         timedelta(seconds=round(time()-initTime)),
                                         round(time()-initTime, 2),
                                         round(self.readyTime-initTime, 2),
                                         round(self.loadTime-self.readyTime, 2)
                                        ),
                                inline=False)
                await m.channel.send('', embed=embed)

            elif cm == "poll":    
                embed = discord.Embed(color=0xb20ac5)
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

            elif cm in self.reDb:
                await m.channel.send(choice(self.reDb[cm]))

            else:
                await m.channel.send(cm + ': command not found')

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]

        elif m.content.startswith("wait, it's all ") and m.content.endswith('?'):
            async with m.channel.typing():
                await sleep(2)
            await m.channel.send('always has been')
            async with m.channel.typing():
                await sleep (3)
            await m.channel.send("I'm sorry "+m.author.name)

        elif "virus" in m.content.lower():
            await m.add_reaction(self.get_emoji(726611950200553502))

        elif "good night" in m.content.lower() or "goodnight" in m.content.lower():
            await m.add_reaction("❤️")


bot = byterbot()
bot.run("NzQwMDA2NDU3ODA1NjM1Njc4.XyiuuA.O2PFUXd4r-GZVfw-g5CZVHMQacc")