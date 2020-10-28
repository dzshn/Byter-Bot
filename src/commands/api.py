import json
from re import sub
from urllib.parse import quote_plus

import discord
import requests

from ..utils import errors


async def avatar(m, text):
    embed = discord.Embed()
    embed.set_image(url=f"https://api.adorable.io/avatars/285/{quote_plus(text)}.png")
    embed.set_footer(text="Powered by avatars.adorable.io")
    await m.channel.send(embed=embed)


async def animal(m, a):
    embed = discord.Embed()
    if a == 0:
        embed.set_image(url=requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url'])
        embed.set_footer(text="Powered by TheCatAPI")

    elif a == 1:
        embed.set_image(url=requests.get("https://random.dog/woof.json").json()['url'])
        embed.set_footer(text="Powered by RandomDog")

    elif a == 2:
        embed.set_image(url=requests.get("https://randomfox.ca/floof/").json()['image'])
        embed.set_footer(text="Powered by RandomFox")

    await m.channel.send(embed=embed)


async def cat(m):
    await animal(m, 0)


async def dog(m):
    await animal(m, 1)


async def fox(m):
    await animal(m, 2)


async def joke(m):
    data = requests.get(
        "https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist").json()

    if data['type'] == 'single':
        embed = discord.Embed(description=data['joke'])

    else:
        embed = discord.Embed(title=data['setup'], description=data['delivery'])

    embed.set_footer(text="Powered by sv443.net's joke API")
    await m.channel.send(embed=embed)


async def name(m, name):
    data = [
        requests.get("https://api.agify.io/?name="+name).json(),
        requests.get("https://api.genderize.io/?name="+name).json(),
        requests.get("https://api.nationalize.io/?name="+name).json()
    ]
    embed = discord.Embed(
        description=(
            f"**Age:** {data[0]['age']}\n"
            f"**Gender:** {data[1]['gender']} (prob. {data[1]['probability']})\n"
            f"**Nationalities:** {', '.join([i['country_id'] for i in data[2]['country']])}"
        )
    )
    embed.set_footer(text="Powered by agify, genderize and nationalize apis")
    await m.channel.send(embed=embed)


async def nasa(m):
    data = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY").json()
    embed = discord.Embed(
        title=data['title'],
        description=f"{data['explanation']}\nDate: {data['date']} | Copyright: {data['copyright']}"
    )
    embed.set_image(url=data['url'])
    embed.set_footer(text="Powered by nasa.gov's api")
    await m.channel.send(embed=embed)


async def qr(m, text):
    embed = discord.Embed()
    embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?data="+text)
    embed.set_footer(text="Powered by goqr.me api")
    await m.channel.send(embed=embed)


async def time(m, args):
    page = '/'.join(args)
    data = requests.get('http://worldtimeapi.org/api/'+page).json()
    embed = discord.Embed(title=page)
    if "datetime" in data:
        embed.description = f"**Current time:** {data['datetime'].split('T')[1][:8]}\n**UTC offset:** {data['utc_offset']}"
        embed.title += "'s current time"

    elif "error" in data:
        embed.description = data['error']
        embed.title += ": error!"

    else:
        embed.description = ', '.join([i.lower().replace(args[0], '').lstrip('/') for i in data])
        embed.title += "'s avaiable timezones"

    embed.set_footer(text="Powered by worldtimeapi.org - bot made by leninnog")
    await m.channel.send(embed=embed)


async def wiki(m, query):
    data = requests.get(
        f"https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=1&srsearch={quote_plus(query)}&srlimit=5&srprop=wordcount|snippet&format=json").json()

    if data['query']['search'] == []:
        await m.channel.send(f"No results for {query}")
        return 1

    embed = discord.Embed(title=f"Search results for {query}")
    embed.set_footer(text='Powered by Wikipedia api')
    for i in data['query']['search']:
        embed.add_field(
            name=i['title'],
            value=f"{sub('<.*?>', '', i['snippet'])}\n[**link**](https://en.wikipedia.org/wiki/{quote_plus(i['title']).replace('+', '_')}"
        )

    await m.channel.send(embed=embed)


async def xkcd(m, ref):
    if ref != None:
        if ref == "c":
            data = requests.get("https://xkcd.com/info.0.json").json()

        else:
            try:
                data = requests.get(f"https://xkcd.com/{ref}/info.0.json").json()

            except json.JSONDecodeError:
                raise errors.CommandError("invalid id")

    else:
        data = requests.get(requests.get("https://c.xkcd.com/random/comic").url+"info.0.json").json()

    embed = discord.Embed(title=data['safe_title'], description=data['alt'])
    embed.set_image(url=data['img'])
    embed.set_footer(text="Powered by xkcd.com")
    await m.channel.send(embed=embed)
