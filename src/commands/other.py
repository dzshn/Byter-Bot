import asyncio
import json
from datetime import timedelta
from re import findall
from secrets import choice
from time import time

import discord
import psutil


async def embed(m, arg):
    embed = discord.Embed()
    data = findall(r"[\w]*:", arg)
    embed.description = "**data :** %s" % data
    await m.channel.send(embed=embed)


async def gifs(m, c):
    await m.channel.send(
        embed=discord.Embed(
            color=0x301baa,
            description=f"**Available categories ({len(c.reDb)}):** `{'`, `'.join(c.reDb.keys())}`"
        ))


async def helpb(m, arg):
    pass


async def info(m, c, arg):
    page = arg.split(' ')
    if page == ['']:
        embed = discord.Embed(
            color=0x301baa,
            title="Info!",
            description="Currently there's info only for characters!\n\nuse `char` or `character` after this command to see it!"
        )
        embed.set_thumbnail(
            url=choice([
                "https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif",
                "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"
            ]))
        embed.set_footer(
            text="creucat.com © PriVer - bot developed by leninnog",
            icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif"
        )

    elif page[0] in ["character", "char"]:
        if len(page) == 1:
            embed = discord.Embed(
                color=0x00002a,
                title="Characters!",
                description="Want to know about the créu characters? this is the way to go!\n\nJust put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course, me!"
            )
            embed.set_thumbnail(
                url=choice([
                    "https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif",
                    "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"
                ]))
            embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                             icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
            await m.channel.send(embed=embed)
            return 1

        elif page[1].lower().replace('&', '').replace('é', 'e') in c.jsonfiles['char']:
            charData = c.jsonfiles['char'][page[1].lower().replace(
                '&', '').replace('é', 'e')]

        else:
            charData = c.jsonfiles['char']['unknown']

        embed = discord.Embed(color=int(charData['color'], 16))
        embed.set_thumbnail(url=charData['thumb'])
        embed.add_field(
            name=charData['name'],
            value=charData['desc'],
            inline=False
        )
        embed.add_field(name="Favorites", value="<:coffee:741469635492446268> %s\n\n<:ice_cream:741469513773613118> %s\n\n<:music:741469877143076946> %s" % tuple(
            charData['favs']), inline=False)
        embed.set_image(url=charData['img'])
        embed.set_footer(
            text="creucat.com/characters © PriVer",
            icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif"
        )

    await m.channel.send(embed=embed)


async def poll(m, c, arg):
    options = [chr(127426+i) for i in range(20)] # unicode "regional_indicator" emojis from A to T
    poll = arg.split(',')
    pollText = ''
    for i in poll[1:]:
        pollText += options[poll[1:].index(i)]+' '+i+'\n'

    if len(poll) == 1:
        pollText = '<:hand_thumbsup:757023230073634922> / <:hand_thumbsdown:757019524058054686>'

    pollMsg = await m.channel.send(
        embed=discord.Embed(
            color=0x301baa, title=poll[0].strip(), description=pollText)
    )
    for i in range(len(poll[1:])):
        await pollMsg.add_reaction(options[i])

    if len(poll) == 1:
        await pollMsg.add_reaction(c.get_emoji(757023230073634922))
        await pollMsg.add_reaction(c.get_emoji(757019524058054686))

    await m.delete()


async def stats(m, c):
    embed = discord.Embed(
        color=0x301baa, title="**Here are some numbers I found**")
    t = time()
    embed.add_field(
        name="**Time Metrics:**",
        value=(
            f"**Total uptime :** {timedelta(seconds=round(t-c.initTime))}\n"
            f"**Last disconnect :** {timedelta(seconds=round(t-c.readyTime))} ago\n"
            f"**Connection load time :** {round(c.readyTime-c.initTime, 2)}s\n"
            f"**Total load time :** {round(c.loadTime-c.readyTime, 2)}s"
        )
    )

    embed.add_field(
        name="**Usage data:**",
        value=(
            f"**Server Count :** {len(c.guilds)}\n"
            f"**Latency :** {round(c.latency, 3)}ms\n"
            f"**CPU :** {psutil.cpu_percent()}\n"
            f"**RAM :** {psutil.virtual_memory().percent}\n"
            f"**Swap :** {psutil.swap_memory().percent}"
        )
    )

    embed.set_footer(text="version %s - bot made by leninnog" % c.version)
    await m.channel.send(embed=embed)


async def userinfo(m):
    await m.channel.send()


async def ball8(m, c):
    ball8msg = None
    while True:
        sball8 = choice(list(c.ball8))
        embed = discord.Embed(color=0x301baa, title=sball8)
        embed.set_image(url=c.ball8[sball8])
        embed.set_footer(text="8ball by zuli - bot by leninnog")
        if ball8msg == None:
            ball8msg = await m.channel.send(embed=embed)

        else:
            await ball8msg.edit(embed=embed)

        if not m.guild.me.permissions_in(m.channel).manage_messages:
            return

        await ball8msg.add_reaction("🔄")

        try:
            r, u = await c.wait_for(
                'reaction_add',
                check=lambda r, u:  str(r.emoji) == "🔄" and r.message.id == ball8msg.id and u == m.author,
                timeout=240
            )

        except asyncio.TimeoutError:
            return

        await r.remove(u)
