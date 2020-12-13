import asyncio
import typing
import os
import secrets
import urllib.parse

import discord
from discord.ext import commands

from . import utils # pylint: disable=relative-beyond-top-level


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _bf(self, code):
        """Internal function for executing brainf code, used only on the command"""
        tape = [0]*256
        tape_pttr = 0
        code_pttr = 0
        out = ''
        braces_openings = [pos for pos, instr in enumerate(code) if instr == '[']
        braces_closings = [pos for pos, instr in enumerate(code) if instr == ']']
        bracemap = {
            **dict(zip(braces_closings, braces_openings)),
            **dict(zip(braces_openings, braces_closings))
        }
        while code_pttr < len(code):
            instruction = code[code_pttr]
            if instruction == '+':
                if tape[tape_pttr] < 255:
                    tape[tape_pttr] += 1

                else:
                    tape[tape_pttr] -= 255

            if instruction == '-':
                if tape[tape_pttr] > 0:
                    tape[tape_pttr] -= 1

                else:
                    tape[tape_pttr] += 255

            if instruction == '>':
                if tape_pttr < 255:
                    tape_pttr += 1

                else:
                    tape_pttr -= 255

            if instruction == '<':
                if tape_pttr > 0:
                    tape_pttr -= 1

                else:
                    tape_pttr += 255

            if instruction == '.':
                out += chr(tape[tape_pttr])

            if instruction == "[" and tape[tape_pttr] == 0:
                code_pttr = bracemap[code_pttr]

            if instruction == "]" and tape[tape_pttr] != 0:
                code_pttr = bracemap[code_pttr]

            code_pttr += 1

        return out

    @commands.command(aliases=['bf'])
    async def brainf(self, ctx, *, code):
        """
        A brainf interpreter

        Code is executed on a 256 length tape, max cell size is 255, timeout is 10 seconds.
        [Wikipedia](https://en.wikipedia.org/wiki/BrainF)
        """
        try:
            out = await asyncio.wait_for(
                self.bot.loop.run_in_executor(None, self._bf, code),
                timeout=10.0
            )

        except asyncio.TimeoutError:
            await ctx.send('Code timed out after 10 seconds')

        else:
            out, att = utils.format_output(out)

            await ctx.send(
                embed=discord.Embed(
                    color=0x05ba05,
                    title=":white_check_mark: BrainF code evaluated with success",
                    description=f"```\n{out}\n```"
                ),
                file=att
            )

    @commands.command(name="8ball")
    async def _8ball(self, ctx):
        """Rolls an 8ball"""
        ball8_db = self.bot.database.ball8_db
        text, img = secrets.choice(list(ball8_db.items()))
        embed = discord.Embed(color=0x301baa, title=text)
        embed.set_image(url=img)
        embed.set_footer(text="8ball images by zuli")
        ball8msg = await ctx.send(embed=embed)
        if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
            await ball8msg.add_reaction("🔄")
            while True:
                try:
                    reaction, user = await self.bot.wait_for(
                        'reaction_add',
                        check=lambda r, u:
                            str(r.emoji) == "🔄" and r.message == ball8msg and u == ctx.author,
                        timeout=240
                    )

                except asyncio.TimeoutError:
                    return

                text, img = secrets.choice(list(ball8_db.items()))
                embed.title = text
                embed.set_image(url=img)
                await ball8msg.edit(embed=embed)
                await reaction.remove(user)

    @commands.command(aliases=["g", "image"])
    async def gifs(self, ctx, name: typing.Optional[str]=None):
        """
        Reaction GIFs and Images

        Run the command to list available GIFs/Images or run it with the reaction name to pick a random one from it
        """
        reaction_db = self.bot.database.reaction_db
        if name is None:
            await ctx.send(
                embed=discord.Embed(
                    title=f"Loaded GIFs/Images ({len(reaction_db)}):\n",
                    description=f"`{'`, `'.join(reaction_db.keys())}`"
                )
            )

        else:
            if name in reaction_db:
                await ctx.send(secrets.choice(reaction_db[name]))

            else:
                await ctx.send(f"Reaction {name} not found :/")

    @commands.command()
    async def name(self, ctx, name: urllib.parse.quote_plus):
        """Returns most probable age and gender for given name"""
        embed = discord.Embed()
        async with self.bot.session.get('https://api.agify.io/?name=' + name) as response:
            if response.status == 200:
                json = await response.json()
                embed.description = f"**Age:** {json['age']}\n"

            else:
                embed.description = "**Age:** Unknown error\n"

        async with self.bot.session.get('https://api.genderize.io/?name=' + name) as response:
            if response.status == 200:
                json = await response.json()
                embed.description += f"**Gender:** {json['gender']} (prob. {json['probability']})\n"

            else:
                embed.description += "**Gender:** Unknown error"

        await ctx.send(embed=embed)

    @commands.command()
    async def urandom(self, ctx, length: typing.Optional[int]=64, encoding: typing.Optional[str]='utf-8'):
        """
        Fresh random bytes from /dev/urandom

        you may optionally pass length (bytes) and encoding, both default to 64 and utf-8
        """
        if length > 2000:
            await ctx.send(f"Length {length} is too big")
            return

        try:
            await ctx.send(os.urandom(length).decode(encoding=encoding, errors='replace'))

        except LookupError:
            await ctx.send(f"Encoding {encoding} isn't valid")


def setup(bot):
    bot.add_cog(Fun(bot))
