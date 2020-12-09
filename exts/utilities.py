import datetime
import json
import typing
import urllib.parse
import re

import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx, *, data):
        """
        Generates an embed

        The data given must be in a "parameter": "value" syntax (aka json)
        valid parameters can be found [here](https://docs.byterbot.com/#extras.embed_params)
        (or in the [Official developer documentation](https://discord.com/developers/docs/resources/channel#embed-object), if you will)

        Example:
        embed "title": "Look!", "description": "I'm a embed!"

        """
        try:
            await ctx.send(embed=discord.Embed.from_dict(json.loads(data)))

        except json.JSONDecodeError:
            await ctx.send("Invalid data given")

    @commands.command()
    async def poll(self, ctx, *, arguments: typing.Optional[str]="Poll"):
        """
        Makes a poll

        Arguments are split by commas, the first one is used as title and others are used as options

        If only title given, options will be thumbs up/down

        If no arguments given, it will default to "Poll"
        """
        # unicode "regional_indicator" emojis from A to T
        options = [chr(127462 + i) for i in range(20)]
        arguments = arguments.split(',')
        embed = discord.Embed(color=0x301baa)
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        if len(arguments) < 2:
            embed.description = '<:hand_thumbsup:757023230073634922> / <:hand_thumbsdown:757019524058054686>'

        else:
            embed.description = '\n'.join([f"{i} {j}" for i, j in zip(options, arguments[1:])])

        if len(arguments) > 0:
            embed.title = arguments[0]

        poll_msg = await ctx.send(embed=embed)

        if len(arguments) < 2:
            await poll_msg.add_reaction(self.bot.get_emoji(757023230073634922))
            await poll_msg.add_reaction(self.bot.get_emoji(757019524058054686))

        else:
            for i in range(len(arguments)-1):
                await poll_msg.add_reaction(options[i])

        await ctx.message.delete()

    @commands.command()
    async def time(self, ctx, *, zone):
        """
        Gets current time for a given timezone

        Available areas are:
        Africa, America, Antarctica, Asia, Atlantic, Australia, CET, CST6CDT,
        EET, EST, EST5EDT, Etc, Europe, HST, Indian, MET, MST, MST7MDT, MST7MDT,
        PST8PDT, Pacific, WET
        """
        async with self.bot.session.get('https://worldtimeapi.org/api/' + zone) as response:
            if response.status == 200:
                json = await response.json()
                if 'datetime' in json:
                    embed = discord.Embed(
                        title=json['timezone'] + "'s info",
                        description=(
                            f"**Current timestamp:** {datetime.datetime.fromtimestamp(json['unixtime'])}\n"
                            f"**UTC offset:** {json['utc_offset']}"
                        )
                    )

                else:
                    embed = discord.Embed(
                        title=zone + "'s available timezones",
                        description=', '.join(i.lower().replace(zone, '').strip('/') for i in json)
                    )

                await ctx.send(embed=embed)

    @commands.command()
    async def wiki(self, ctx, max_results: typing.Optional[int]=3, *, query: urllib.parse.quote_plus):
        """
        Searches wikipedia

        Max results needs to be between 1 and 5
        """
        if not 0 < max_results < 6:
            raise commands.UserInputError('Max results must be between 1 and 5')

        params = {
            "action": "query",
            "list": "search",
            "utf8": 1,
            "srsearch": query,
            "srlimit": max_results,
            "srprop": "wordcount|snippet",
            "format": "json"
        }

        async with self.bot.session.get(f"https://en.wikipedia.org/w/api.php", params=params) as response:
            if response.status == 200:
                json = await response.json()
                embed = discord.Embed(title=f'Search results for {query}')
                for data in json['query']['search']:
                    embed.add_field(
                        name=data['title'],
                        value=(
                            f"{re.sub('<.*?>', '', data['snippet'])}\n" # clean up html tags
                            "[**link**](https://en.wikipedia.org/wiki/"
                                f"{urllib.parse.quote(data['title']).replace(' ', '_')}"
                            ")"
                        )
                    )

                await ctx.send(embed=embed)

            else:
                await ctx.send('Something went wrong')


def setup(bot):
    bot.add_cog(Utils(bot))
