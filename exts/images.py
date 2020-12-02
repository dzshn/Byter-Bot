import json
import typing
import urllib.parse

import discord
from discord.ext import commands


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command()
    async def cat(self, ctx):
        """Returns a random cat image"""
        embed = discord.Embed()
        async with self.session.get("https://api.thecatapi.com/v1/images/search") as response:
            if response.status == 200:
                json = await response.json()
                embed.set_image(url=json[0]['url'])

            else:
                await ctx.send('Something went wrong while requesting your cat')
                return

        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        """Returns a random dog image"""
        embed = discord.Embed()
        async with self.session.get("https://random.dog/woof.json") as response:
            if response.status == 200:
                json = await response.json()
                embed.set_image(url=json['url'])

            else:
                await ctx.send('Something went wrong while requesting your dog')
                return

        await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        """Returns a random fox image"""
        embed = discord.Embed()
        async with self.session.get("https://randomfox.ca/floof/") as response:
            if response.status == 200:
                json = await response.json()
                embed.set_image(url=json['image'])

            else:
                await ctx.send('Something went wrong while requesting your fox')
                return

        await ctx.send(embed=embed)

    @commands.command()
    async def qr(self, ctx, *, text: urllib.parse.quote_plus):
        """Generates a qr code with given text"""
        embed = discord.Embed()
        embed.set_image(
            url=f"https://api.qrserver.com/v1/create-qr-code/?data={text}"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def xkcd(self, ctx, ref: typing.Optional[str.lower]="random"):
        """
        Returns an xkcd comic

        ref may be "random", "current" or an comic id, defaults to random
        """
        embed = discord.Embed()
        if ref == "random":
            async with self.session.get("https://c.xkcd.com/random/comic") as rand_redir:
                async with self.session.get(f"{rand_redir.url}info.0.json") as response:
                    if response.status == 200:
                        json = await response.json()

        elif ref == "current":
            async with self.session.get("https://xkcd.com/info.0.json") as response:
                if response.status == 200:
                    json = await response.json()

        elif ref.isdecimal():
            async with self.session.get(f"https://xkcd.com/{ref}/info.0.json") as response:
                if response.status == 200:
                    json = await response.json()

        else:
            raise commands.UserInputError(message="Invalid ref given")

        embed = discord.Embed(title=json['safe_title'], description=json['alt'])
        embed.set_image(url=json['img'])
        embed.set_footer(text="Powered by xkcd.com")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
