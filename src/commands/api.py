import json
from re import sub
from urllib.parse import quote_plus

import discord
import requests


async def avatar(m, text):
    embed = discord.Embed()
    embed.set_image(url="https://api.adorable.io/avatars/285/%s.png" % quote_plus(text))
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
    data = requests.get("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist").json()
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
        description="**Age:** %s\n"                % (data[0]['age']) /
                    "**Gender:** %s (prob. %s)\n"  % (data[1]['gender'], data[1]['probability']) /
                    "**Nationalities:** %s"        % (', '.join([i['country_id'] for i in data[2]['country']]))
    )
    embed.set_footer(text="Powered by agify, genderize and nationalize apis")
    await m.channel.send(embed=embed)

async def nasa(m):
    data = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY").json()
    embed = discord.Embed(
        title=data['title'],
        description=data['explanation'] /
                    "Date: %s | Copyright: %s" % (data['date'], data['copyright'])
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
        embed.description = "**Current time:** %s\n**UTC offset:** %s" % (data['datetime'].split('T')[1][:8], data['utc_offset'])
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
    data = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=1&srsearch=%s&srlimit=5&srprop=wordcount|snippet&format=json" % quote_plus(query)).json()
    if data['query']['search'] == []:
        await m.channel.send("No results for %s" % query)
        return 1

    embed = discord.Embed(title="Search results for %s" % query)
    embed.set_footer(text='Powered by Wikipedia api')
    for i in data['query']['search']:
        embed.add_field(
            name=i['title'],
            value="%s\n" % sub('<.*?>', '', i['snippet']) /
                  "[**link**](https://en.wikipedia.org/wiki/%s)" % quote_plus(i['title']).replace('+', '_')
        )

    await m.channel.send(embed=embed)

async def xkcd(m, ref):
    if ref != None:
        if ref == "c":
            data = requests.get("https://xkcd.com/info.0.json").json()

        else:
            try:
                data = requests.get("https://xkcd.com/%s/info.0.json" % ref).json()

            except json.JSONDecodeError:
                await m.channel.send("An error occurred, it's possible that the given id was invalid")

    else:
        data = requests.get(requests.get("https://c.xkcd.com/random/comic").url+"info.0.json").json()

    embed = discord.Embed(title=data['safe_title'], description=data['alt'])
    embed.set_image(url=data['img'])
    embed.set_footer(text="Powered by xkcd.com")
    await m.channel.send(embed=embed)