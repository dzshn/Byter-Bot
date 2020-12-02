import discord
from discord.ext import commands

class CreuServerStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cguild = self.bot.get_guild(725421276562325514)

    @commands.Cog.listener()
    async def on_ready(self):
        self.cguild = self.bot.get_guild(725421276562325514)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and self.bot.get_user(self.bot.owner_id) in message.mentions:
            await message.add_reaction(self.bot.get_emoji(748824813501546559))

        if message.guild == self.cguild:
            lowered = message.content.lower()
            if "good night" in lowered or "goodnight" in lowered or "qnight" in lowered:
                await message.add_reaction("❤️")

            if "dreamworks" in lowered or  "poop" in lowered:
                await message.add_reaction(self.bot.get_emoji(726611950200553502))

    @commands.command(hidden=True)
    async def mewhen(self, ctx):
        """me when"""
        await ctx.send(
            embed=discord.Embed(title="me when").set_image(
                url="https://cdn.discordapp.com/attachments/775223088534388767" \
                    "/775223895786782730/Speedy_Creu_but_Bigger.gif"
        ))


def setup(bot):
    bot.add_cog(CreuServerStuff(bot))
