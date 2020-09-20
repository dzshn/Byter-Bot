#!/usr/bin/env python3
from urllib.parse import quote_plus
from datetime import timedelta
from secrets import choice
from sys import exc_info
from time import time
from re import sub
import emailhandler
import numpy as np
import traceback
import threading
import requests
import asyncio
import discord
import psutil
import json
import math
import os

initTime = time()

tkn = open("TOKEN").read()

class byterbot(discord.Client):
    reDb = {}
    ball8 = {}

    readyTime = 0
    loadTime = 0

    jsonfiles = {
        i:json.load(open(json.load(open('data/index.json'))[i]))
        for i in json.load(open('data/index.json'))
    }

    version = open('VERSION').read()

    async def on_ready(self):
        self.readyTime = time()
        async for i in self.get_channel(740539699134857337).history():
            if i.content in self.reDb:
                self.reDb[i.content].append(i.attachments[0].url)

            else:
                self.reDb[i.content] = [i.attachments[0].url]

        async for i in self.get_channel(742479941504860341).history():
            self.ball8[i.content] = i.attachments[0].url

        emailthread = threading.Thread(target=await emailhandler.start(self.get_channel(754876413043146823)))
        emailthread.run()

        self.loadTime = time()

    async def on_message(self, m):
        if m.author.bot and m.webhook_id != 740524198165872711:
            return 1

        if m.channel.id == 740078363191935079 and self.user.id == 740006457805635678:
            return 1

        elif m.content.startswith(('%', 'b!')):
            ctx = m.content[1:].split(' ') if m.content.startswith('%') else m.content[2:].split(' ')
            cm = ctx[0]

            if cm == "api":
                if len(ctx) == 1:
                    await m.channel.send(
                        embed=discord.Embed(
                            title="Apis!",
                            description='''
Apis, short for Application Programming Interface, is a way of code to interact to a service, like I do for %time or the auto-translator
here in this command will be a bunch of apis that I don't think need to have a command, the list is as it follows:

avatar, cat, dog, fox, joke, name, nasa, qr, wikipedia, xkcd

you can use `%help api <apiName>` to see how one in specific works
                            '''
                        )
                    )

                else:
                    if ctx[1] == "avatar":
                        embed = discord.Embed()
                        if len(ctx) == 2:
                            embed.set_image(url="https://api.adorable.io/avatars/285/%s.png" % m.author.name)

                        else:
                            embed.set_image(url="https://api.adorable.io/avatars/285/%s.png" % quote_plus(''.join(ctx[2:])))

                        embed.set_footer(text="Powered by avatars.adorable.io")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "cat":
                        embed = discord.Embed()
                        embed.set_image(url=requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url'])
                        embed.set_footer(text="Powered by TheCatAPI")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "dog":
                        embed = discord.Embed()
                        embed.set_image(url=requests.get("https://random.dog/woof.json").json()['url'])
                        embed.set_footer(text="Powered by RandomDog")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "fox":
                        embed = discord.Embed()
                        embed.set_image(url=requests.get("https://randomfox.ca/floof/").json()['image'])
                        embed.set_footer(text="Powered by RandomFox")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "joke":
                        data = requests.get("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist").json()
                        if data['type'] == 'single':
                            embed = discord.Embed(description=data['joke'])

                        else:
                            embed = discord.Embed(title=data['setup'], description=data['delivery'])

                        embed.set_footer(text="Powered by sv443.net's joke API")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "name":
                        data = [
                            requests.get("https://api.agify.io/?name="+''.join(ctx[2:])).json(),
                            requests.get("https://api.genderize.io/?name="+''.join(ctx[2:])).json(),
                            requests.get("https://api.nationalize.io/?name="+''.join(ctx[2:])).json()
                        ]
                        embed = discord.Embed(
                            description="**Age:** %s\n**Gender:** %s (prob. %s)\n**Nationalities:** %s" % (
                                data[0]['age'], data[1]['gender'], data[1]['probability'],
                                ', '.join(['%s (prob %s)' % (i['country_id'], round(i['probability'], 3)) for i in data[2]['country']])
                            )
                        )
                        embed.set_footer(text="Powered by agify, genderize and nationalize apis")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "nasa":
                        data = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY").json()
                        embed = discord.Embed(
                            title=data['title'],
                            description="%s\nDate: %s | Copyright: %s" % (data['explanation'], data['date'], data['copyright'])
                        )
                        embed.set_image(url=data['url'])
                        embed.set_footer(text="Powered by nasa.gov's api")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "qr":
                        if len(ctx) == 2:
                            await m.channel.send(embed=discord.Embed(title='QR codes', description="a simple way to generate qr codes, just use your text after this command"))

                        else:
                            embed = discord.Embed()
                            embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?data="+quote_plus(''.join(ctx[2:])))
                            embed.set_footer(text="Powered by goqr.me api")
                            await m.channel.send(embed=embed)

                    elif ctx[1] == "time":
                        if len(ctx) == 2:
                            embed = discord.Embed(
                                title="Timezones!",
                                description='''
Shows current time in a given area

The avaiable areas are: Africa, America, Antartica, Asia, Atlantic, Australia, CET, CST6CDT, EET, EET5EDT, Etc, Europe, HST, Indian, MET, MST, MST5MDT, PST8PDT, Pacific and WET
                                '''
                            )

                        else:
                            page = '/'.join(ctx[2:])
                            data = requests.get('http://worldtimeapi.org/api/'+page).json()
                            embed = discord.Embed(title=page)
                            if "datetime" in data:
                                embed.description = "**Current time:** %s\n**UTC offset:** %s" % (
                                    data['datetime'].split('T')[1][:8], data['utc_offset']
                                )
                                embed.title += "'s current time"

                            elif "error" in data:
                                embed.description = data['error']
                                embed.title += ": error!"

                            else:
                                embed.description = ', '.join([i.lower().replace(ctx[2], '').lstrip('/') for i in data])
                                embed.title += "'s avaiable timezones"

                        embed.set_footer(text="Powered by worldtimeapi.org - bot made by leninnog")
                        await m.channel.send(embed=embed)

                    elif ctx[1] == "wikipedia":
                        if len(ctx) == 2:
                            await m.channel.send(embed=discord.Embed(title='Wikipedia', description="Wikipedia search, simple, right?"))
                            return 1

                        data = requests.get(
                            "https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=1&srsearch=%s&srlimit=5&srprop=wordcount|snippet&format=json"
                            % quote_plus(''.join(ctx[2:]))
                        ).json()
                        if data['query']['search'] == []:
                            await m.channel.send("No results for %s" % ''.join(ctx[2:]))
                            return 1

                        embed = discord.Embed(title="Search results for "+''.join(ctx[2:]))
                        embed.set_footer(text='Powered by Wikipedia api')
                        for i in data['query']['search']:
                            embed.add_field(
                                name="**%s**" % i['title'],
                                value="%s\n[**link**](https://en.wikipedia.org/wiki/%s) **words:** %s" % (
                                    sub('<.*?>', '', i['snippet']),
                                    i['wordcount'],
                                    quote_plus(i['title']).replace('+', '_')
                                )
                            )

                        await m.channel.send(embed=embed)

                    elif ctx[1] == "xkcd":
                        if len(ctx) == 3:
                            if ctx[2] == "current":
                                data = requests.get("https://xkcd.com/info.0.json").json()
                            elif ctx[2].isdecimal():
                                try:
                                    data = requests.get("https://xkcd.com/%s/info.0.json" % ctx[2]).json()

                                except json.JSONDecodeError:
                                    await m.channel.send("An error occurred, it's possible that the given id was invalid")
                                    return 1

                        else:
                            data = requests.get(requests.get("https://c.xkcd.com/random/comic").url+"info.0.json").json()

                        embed = discord.Embed(title=data['safe_title'], description=data['alt'])
                        embed.set_image(url=data['img'])
                        embed.set_footer(text="Powered by xkcd.com")
                        await m.channel.send(embed=embed)

            elif cm == "embed":
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

%embed "title": "Example Title", "description": "Example desc"

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
                        if "file" in self.jsonfiles['help'][ctx[1]]:
                            file = self.jsonfiles[self.jsonfiles['help'][ctx[1]]['file']]
                            if len(ctx) == 2:
                                data = file['index']

                            elif ctx[2] in file:
                                data = file[ctx[2]]

                            else:
                                await m.channel.send('help: %s: %s: page not found' % (ctx[1], ctx[2]))
                                return 1

                        else:
                            data = self.jsonfiles['help'][ctx[1]]

                    else:
                        await m.channel.send('help: %s: page not found' % ctx[1])
                        return 1

                embed = discord.Embed(color=0x301baa, title=data['title'], description='\n'.join(data['description']))
                await m.channel.send(embed=embed)

            elif cm == "info":
                if len(ctx) == 1:
                    embed = discord.Embed(
                        color=0x301baa, title="Info!",
                        description="Currently there's info only for characters!\n\nuse `char` or `character` after this command to see it!"
                    )
                    embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                    embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                     icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")

                elif ctx[1] in ["character", "char"]:
                    if len(ctx) == 2:
                        embed = discord.Embed(
                            color=0x00002a, title="Characters!",
                            description="Want to know about the créu characters? this is the way to go!\n\nJust put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course, me!"
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

            elif cm == "minigame":
                if len(ctx) == 1:
                    await m.channel.send(
                        embed=discord.Embed(
                            title="Minigames!",
                            description='''
Bored? try some minigames! currently there's only 2048 and tictactoe _but_ there will be more in the future!
                            '''
                        )
                    )
                    return 1

                elif ctx[1] == "2048":
                    gameDat = np.array([[0 for i in range(4)] for ii in range(4)])
                    gameScr = 0
                    gameDat.flat[choice([i for i, j in enumerate(gameDat.flatten()) if j == 0])] = choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
                    gameDsp = lambda : '\n'.join([
                        ''.join([
                            self.jsonfiles['ming']['2048']['tiles'][n] for n in gameDat[i]
                        ]) for i in range(4)
                    ])
                    gameEmb = discord.Embed()
                    gameEmb.add_field(name="2048!", value=gameDsp())
                    gameEmb.add_field(name="Score", value=gameScr)
                    gEmbUpd = lambda : (
                        gameEmb.set_field_at(0, name="2048!", value=gameDsp()),
                        gameEmb.set_field_at(1, name="Score", value=gameScr)
                    )
                    gameMsg = await m.channel.send(embed=gameEmb)
                    [await gameMsg.add_reaction(i) for i in ['⬆️', '⬇️', '⬅️', '➡️']]
                    while 0 in gameDat:
                        try:
                            r, u = await self.wait_for(
                                "reaction_add",
                                check=lambda r, u: str(r.emoji) in ['⬆️', '⬇️', '⬅️', '➡️'] and r.message.id == gameMsg.id and u == m.author,
                                timeout=120
                            )

                        except asyncio.TimeoutError:
                            await m.channel.send('× -× timed out')
                            return 1

                        await r.remove(u)

                        def move(gdat, gscr, ay, ax, r1=0, r2=4, r3=0, r4=4):
                            for i in range(4):
                                for iy in range(r1, r2):
                                    for ix in range(r3, r4):
                                        if gdat[iy][ix] != 0:
                                            if gdat[iy+ay][ix+ax] == 0:
                                                gdat[iy+ay][ix+ax] = gdat[iy][ix]
                                                gdat[iy][ix] = 0

                                            elif gdat[iy+ay][ix+ax] == gdat[iy][ix]:
                                                gdat[iy+ay][ix+ax] += 1
                                                gdat[iy][ix] = 0
                                                gscr += 2**gdat[iy+ay][ix+ax]

                            return gdat, gscr

                        if str(r.emoji) == '⬆️':   gameDat, gameScr = move(gameDat, gameScr, -1, 0, r1=1)
                        elif str(r.emoji) == '⬇️': gameDat, gameScr = move(gameDat, gameScr, 1,  0, r2=3)
                        elif str(r.emoji) == '⬅️': gameDat, gameScr = move(gameDat, gameScr, 0, -1, r3=1)
                        elif str(r.emoji) == '➡️': gameDat, gameScr = move(gameDat, gameScr, 0,  1, r4=3)

                        await gameMsg.edit(embed=gameEmb)
                        await asyncio.sleep(.05)
                        gameDat.flat[choice([i for i, j in enumerate(gameDat.flatten()) if j == 0])] = 1
                        gEmbUpd()
                        await gameMsg.edit(embed=gameEmb)

                    await gameMsg.edit(embed=discord.Embed(title="Game over , -,", description="Played by: %s\n%s\n**Score:** %s" % (m.author.name, gameDsp(), gameScr)))

                elif ctx[1] == "tictactoe":
                    if len(m.mentions) == 0:
                        await m.channel.send('Please ping someone within the message to play')
                        return 1

                    elif len(m.mentions) > 1:
                        await m.channel.send('Please ping only one person')
                        return 1

                    elif m.mentions[0] == m.author:
                        await m.channel.send('https://media.discordapp.net/attachments/639603988295188519/754816409820856351/Screenshot_20200913_181339.png')
                        return 1

                    gameMsg = await m.channel.send(embed=discord.Embed(
                        description='Waiting for acception, %s, please react with ✅ to accept' % m.mentions[0].name
                    ))
                    await gameMsg.add_reaction('✅')
                    try:
                        await self.wait_for('reaction_add', check=lambda r, u : str(r.emoji) == '✅' and u == m.mentions[0], timeout=60)

                    except asyncio.TimeoutError:
                        await gameMsg.edit(embed=discord.Embed(description='Acception timed out'))
                        return 1

                    crrntPl = choice([1, 2])
                    players = [m.author, m.mentions[0]]
                    gameDat = np.zeros((3, 3), dtype=int)
                    gameDsp = lambda : '\n'.join([
                        ''.join([
                            [':white_large_square:', ':x:', ':o:'][n] for n in gameDat[i]
                        ]) for i in range(3)
                    ]) + ("\n%s's turn" % players[crrntPl-1] if crrntPl != 0 else '')
                    gameEmb = discord.Embed()
                    gameEmb.add_field(name='Tic-Tac-Toe!', value=gameDsp())
                    winCmbs = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
                    await gameMsg.edit(embed=gameEmb)
                    while 0 in gameDat:
                        try:
                            mm = await self.wait_for('message',
                                check=lambda mm: mm.author == players[crrntPl-1] and mm.content in [str(i) for i in range(1, 10)],
                                timeout=240)

                        except asyncio.TimeoutError:
                            await m.channel.send("× -× timed out")
                            return 1

                        if gameDat.flat[int(mm.content)-1] != 0:
                            await m.channel.send("invalid move!")

                        else:
                            gameDat.flat[int(mm.content)-1] = crrntPl
                            crrntPl = 1 if crrntPl == 2 else 2
                            await mm.delete()
                            if any([all([gameDat.flat[j] == 1 for j in i]) for i in winCmbs]):
                                crrntPl = 0
                                gameEmb.set_field_at(0, name="Game over", value=gameDsp())
                                gameEmb.add_field(name="%s wins!" % players[0].name,
                                    value='played by %s and %s' % (players[0].name, players[1].name))

                            elif any([all([gameDat.flat[j] == 2 for j in i]) for i in winCmbs]):
                                crrntPl = 0
                                gameEmb.set_field_at(0, name="Game over", value=gameDsp())
                                gameEmb.add_field(name="%s wins!" % players[1].name,
                                    value='played by %s and %s' % (players[0].name, players[1].name))

                            else:
                                gameEmb.set_field_at(0, name="Tic-Tac-Toe!", value=gameDsp())
                                await gameMsg.edit(embed=gameEmb)

                    gameEmb.set_field_at(0, name="Game over", value=gameDsp())
                    gameEmb.add_field(name="Tie!", value="played by %s and %s" % (players[0].name, players[1].name))
                    await gameMsg.edit(embed=gameEmb)

                elif ctx[1] == "simon":
                    sequence = [choice([0, 1, 2, 3])]
                    gameDat = [0 for i in range(4)]
                    gameDsp = lambda : '%s%s\n%s%s' % (
                        ':green_square:'  if gameDat[0] == 0 else ':white_large_square:',
                        ':red_square:'    if gameDat[1] == 0 else ':white_large_square:',
                        ':yellow_square:' if gameDat[2] == 0 else ':white_large_square:',
                        ':blue_square:'   if gameDat[3] == 0 else ':white_large_square:'
                    )
                    gameMsg = await m.channel.send(embed=discord.Embed(title="Simon!", description=gameDsp()))
                    [await gameMsg.add_reaction(i) for i in ['🟩', '🟥', '🟨', '🟦']]
                    await asyncio.sleep(0.1)
                    while True:
                        for i in sequence:
                            gameDat[i] = 1
                            await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()))
                            await asyncio.sleep(0.1)
                            gameDat[i] = 0
                            await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()))
                            await asyncio.sleep(0.1)

                        await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()+'\nYour turn'))

                        for i in sequence:
                            try:
                                r, u = await self.wait_for('reaction_add',
                                    check=lambda r, u: u == m.author and str(r.emoji) in ['🟩', '🟥', '🟨', '🟦'],
                                    timeout=240
                                )

                            except asyncio.TimeoutError:
                                await gameMsg.edit(embed=discord.Embed(title="Timed out × -×",
                                    description=''.join([
                                        [':green_square:', ':red_square:', ':yellow_square:', ':blue_square:'][i] for i in sequence
                                ])))

                            await r.remove(u)
                            if str(r.emoji) != ['🟩', '🟥', '🟨', '🟦'][i]:
                                await gameMsg.edit(embed=discord.Embed(title="Game over , -,",
                                    description=''.join([
                                        [':green_square:', ':red_square:', ':yellow_square:', ':blue_square:'][ii] for ii in sequence
                                ])))
                                return 1

                        sequence.append(choice([0, 1, 2, 3]))
                        await asyncio.sleep(0.5)

                else:
                    await m.channel.send('minigame: minigame %s not found' % ctx[1])

            elif cm == "poll":
                options = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷' ,'🇸', '🇹']
                poll = m.content.replace('b!', '%')[5:].split(',')
                pollText = ''
                for i in poll[1:]:
                    pollText += options[poll[1:].index(i)]+' '+i+'\n'

                if len(poll) == 1:
                    pollText = '<:hand_thumbsup:757023230073634922> / <:hand_thumbsdown:757019524058054686>'

                pollMsg = await m.channel.send(
                    embed=discord.Embed(color=0x301baa, title=poll[0].strip(), description=pollText)
                )
                for i in range(len(poll[1:])):
                    await pollMsg.add_reaction(options[i])

                if len(poll) == 1:
                    await pollMsg.add_reaction(self.get_emoji(757023230073634922))
                    await pollMsg.add_reaction(self.get_emoji(757019524058054686))

                await m.delete()

            elif cm == "stats":
                embed = discord.Embed(color=0x301baa, title="**Here are some numbers I found**")

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
                        len(self.guilds), psutil.cpu_percent(), psutil.virtual_memory().percent, psutil.swap_memory().percent
                    )
                )

                embed.set_footer(text="version %s - bot made by leninnog" % self.version)
                await m.channel.send(embed=embed)

            elif cm == "8ball":
                ball8msg = None
                while True:
                    sball8 = choice(list(self.ball8))
                    embed = discord.Embed(color=0x301baa, title=sball8)
                    embed.set_image(url=self.ball8[sball8])
                    embed.set_footer(text="8ball by zuli - bot by leninnog")
                    if ball8msg == None:
                        ball8msg = await m.channel.send(embed=embed)

                    else:
                        await ball8msg.edit(embed=embed)

                    if not m.guild.me.permissions_in(m.channel).manage_messages:
                        return 1

                    await ball8msg.add_reaction("🔄")

                    try:
                        r, u = await self.wait_for(
                            'reaction_add', 
                            check=lambda r, u:  str(r.emoji) == "🔄" and r.message.id == ball8msg.id and u == m.author, 
                            timeout=240)

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
                os.execl("./main.py", "main")

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]

        elif self.user.id == 740006457805635678 and m.channel in self.get_channel(741765710971142175).channels and m.channel.id != 745400744303394917:
            data = requests.get('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='+quote_plus(m.clean_content)).content.decode()
            embed = discord.Embed(
                color=0x301baa,
                title="from channel "+m.channel.name,
                description='''
**message content:** %s
**from:** %s
**translation:** %s
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
            embed.description = "**Message content :** %s\n%s" % (args[0].content, embed.description)

        else:
            embed.description = "**Function :** %s\n\n**Args :** %s\n\n**Kwargs :** %s\n%s" % (func, args, kwargs, embed.description)

        await self.get_channel(741024906774577201).send(self.get_user(310449948011528192).mention, embed=embed)

bot = byterbot()
bot.run(tkn)