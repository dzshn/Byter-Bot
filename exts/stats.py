import sys
from time import time
from datetime import timedelta

import discord
import psutil
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_hit = 0
        self.commands_done = 0
        self.version = open("VERSION").read()

    @commands.Cog.listener()
    async def on_command(self, _):
        self.commands_hit += 1

    @commands.Cog.listener()
    async def on_command_completion(self, _):
        self.commands_done += 1

    @commands.command(aliases=['status', 's'])
    async def stats(self, ctx):
        """Returns multiple stats for the bot"""
        embed = discord.Embed(title="Here's some numbers I found")
        proc = psutil.Process()
        upt = round(time()-proc.create_time())
        embed.add_field(
            name="General",
            value=(
                f"**Commands hit/done:** {self.bot.commands_hit}/{self.bot.commands_done}\n"
                f"**Uptime:** {timedelta(seconds=upt)}\n"
                f"**Server Count:** {len(self.bot.guilds)}\n"
                f"**Latency:** {round(self.bot.latency*1000)}ms\n"
            )
        )

        embed.add_field(
            name="Resource usage",
            value=(
                f"**CPU:** {psutil.cpu_percent()}%\n"
                f"**RAM:** {psutil.virtual_memory().percent}%\n"
            )
        )

        embed.set_footer(text=f"Version {self.version}")

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                description=(
                    "Want me on your server?\n"
                    f"[Click here to invite me!](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=388160&scope=bot)"
                )
            )
        )

    @commands.command(name='version')
    async def _version(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                description=(
                    f"**Bot :** {self.version}\n"
                    f"**Python :** {'{}.{}.{} {}'.format(*sys.version_info)}\n"
                    f"**discord.py :** {discord.__version__}\n"
                    f"**psutil :** {psutil.__version__}\n"
                )
            )
        )


def setup(bot):
    bot.add_cog(Stats(bot))
