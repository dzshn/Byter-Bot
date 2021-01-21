import json

import discord
from discord.ext import commands


class CreuServerStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cguild = self.bot.get_guild(725421276562325514)
        try:
            self.reactions = json.load(open('reactions.json'))

        except FileNotFoundError:
            self.reactions = []
            open('reactions.json', 'w')

    @commands.Cog.listener()
    async def on_ready(self):
        self.cguild = self.bot.get_guild(725421276562325514)

    async def do_reactions(self, message):
        if not message.author.bot and self.bot.get_user(self.bot.owner_id) in message.mentions:
            await message.add_reaction(self.bot.get_emoji(748824813501546559))

        if message.guild == self.cguild:
            lowered = ''.join(i for i in message.clean_content.lower() if i in 'abcdefghijklmnopqrstuvwxyz')
            for obj in self.reactions:
                for trigger in obj['triggers']:
                    if trigger in lowered:
                        await message.add_reaction(self.bot.get_emoji(obj['reaction']))
                        break

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.do_reactions(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.do_reactions(after)

    @commands.command(hidden=True)
    async def mewhen(self, ctx):
        """me when"""
        await ctx.send(
            embed=discord.Embed(title="me when").set_image(
                url="https://cdn.discordapp.com/attachments/775223088534388767" \
                    "/775223895786782730/Speedy_Creu_but_Bigger.gif"
            )
        )

    @commands.command(aliases=['z'], hidden=True)
    async def zxyvw(self, ctx, *, text):
        """z"""
        if [z for z in text if z not in 'z0123456789abcdef']:
            await ctx.send('z'.join(f"{ord(z):x}" for z in text))

        else:
            await ctx.send(
                embed=discord.Embed(
                    color=0x301baa,
                    title='z',
                    description=''.join(chr(int(z, base=16)) for z in text.split('z'))
                )
            )


def setup(bot):
    bot.add_cog(CreuServerStuff(bot))
