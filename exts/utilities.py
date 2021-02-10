import datetime
import json
import typing
import urllib.parse
import re

import discord
from discord.ext import commands

from . import utils # pylint: disable=relative-beyond-top-level


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bin'])
    async def binary(self, ctx, *, text : str):
        """
        Binary encoder and decoder

        If given text is detected as binary code it gets decoded, if not I encode the text
        """
        if [i for i in text if i not in (' ', '0', '1')]:
            out, att = utils.format_output(' '.join(f'{ord(char):0>8b}' for char in text))
            await ctx.send(
                embed=discord.Embed(
                    color=0x05ba05,
                    title="Binary output",
                    description=f"```{out}```"
                ),
                file=att
            )

        else:
            text = text.replace(' ', '')
            out, att = utils.format_output(
                ''.join(
                    chr(int(text[i:i+8], base=2))
                    for i in range(0, len(text), 8) 
                )                
            )
            await ctx.send(
                embed=discord.Embed(
                    color=0x05ba05,
                    title="Decoded output",
                    description=f"```{out}```"
                ),
                file=att
            )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, data):
        """
        Generates an embed

        The data given must be in a "parameter": "value" syntax (aka json)
        valid parameters can be found [here](https://docs.byterbot.com/#extras.embed_params)
        (or in the [Official developer documentation](https://discord.com/developers/docs/resources/channel#embed-object), if you will)

        Requires "Manage messages" permissions

        Example:
        embed "title": "Look!", "description": "I'm a embed!"

        """
        try:
            await ctx.send(embed=discord.Embed.from_dict(json.loads('{'+data+'}')))

        except (json.JSONDecodeError, discord.errors.HTTPException):
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

    @commands.command()
    async def userinfo(self, ctx, user: typing.Optional[discord.Member]=None):
        """Return some info about given user / you"""
        user = ctx.author if user == None else user
        await ctx.send(
            embed=discord.Embed(
                color=ctx.author.color.value,
                title=f"Info for {user}" + (f" ({user.nick})" if user.nick else ''),
                description=(
                    f"**ID:** {user.id}\n"
                    f"**Created at:** {user.created_at}\n"
                    f"**Joined at:** {user.joined_at}\n"
                    f"**Roles:** {', '.join([i.name for i in user.roles[1:]]) if user.roles else 'none'}\n"
                )
            ).set_thumbnail(
                url=user.avatar_url
            ).set_footer(
                text=f"Fetched at {datetime.datetime.now()} by {ctx.author}"
            )
        )


def setup(bot):
    bot.add_cog(Utils(bot))
