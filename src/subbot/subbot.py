import json
from urllib.parse import quote_plus

import discord
import requests


client = discord.Client(intents=discord.Intents(guild_messages=True, guilds=True))

@client.event
async def on_message(m):
    if m.channel in client.get_channel(741765710971142175).channels and m.channel.id != 745400744303394917:
        data = requests.get('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q='+quote_plus(m.clean_content)).content.decode()
        embed = discord.Embed(
            color=0x301baa, 
            title="from channel %s" % m.channel.name, 
            description="**message content:** %s\n" % m.content     +
                        "**from:** %s\n"            % m.author.name +
                        "**translation:** %s"       % json.loads(data)[0][0][0]
        )
        embed.set_footer(text="Powered by Google Translate")
        await client.get_channel(745400744303394917).send(embed=embed)

    elif client.get_user(310449948011528192) in m.mentions and not m.author.bot:
        await m.add_reaction(client.get_emoji(748824813501546559))

    elif ("good night" in m.content.lower() or "goodnight" in m.content.lower()):
        await m.add_reaction("❤️")

    elif "dreamworks" in m.content.lower():
        await m.add_reaction(client.get_emoji(726611950200553502))


async def run():
    client.run(open("TOKEN").read())