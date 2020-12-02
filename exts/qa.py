import random
from io import BytesIO

import discord
from discord.ext import commands


class Qa(commands.Cog, command_attrs={'hidden': True}):
    def __init__(self, bot):
        self.bot = bot
        self.is_qa_running = False
        self.creu_guild = None
        self.allowed_roles = None
        self.questions = None

    @commands.group()
    async def qa(self, ctx):
        """Commands used for an Q&A event"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing subcommand")

    @qa.command(name="start")
    @commands.is_owner()
    async def qa_start(self, ctx):
        """Starts up the Q&A session"""
        self.is_qa_running = True
        self.creu_guild = self.bot.get_guild(725421276562325514)
        self.allowed_roles = [
            self.creu_guild.get_role(728875097808699473),
            self.creu_guild.get_role(726615159459676180)
        ]
        self.questions = []
        await ctx.send("All set!")

    @qa.command(name="stop")
    @commands.is_owner()
    async def qa_stop(self, ctx):
        """Stops the Q&A session"""
        async with ctx.channel.typing():
            await ctx.send("Dumping data...")
            await ctx.send(
                file=discord.File(
                    BytesIO(
                        ('-------------\n'.join([f"From: {i['from']}\nQuestion: {i['question']}" for i in self.questions])).encode()
                    ),
                    filename="qadump.txt"
                )
            )
            self.is_qa_running = False
            self.questions = None
            await ctx.send("All clear!")

    @qa.command(name="ask")
    async def qa_ask(self, ctx, *, question):
        """Ask a question, which later be picked at random"""
        if self.is_qa_running:
            self.questions.append({"from": ctx.author, "question": question})

        else:
            await ctx.send("Ey! there isn't a Q&A session yet")

    @qa.command(name="pick")
    async def qa_pick(self, ctx):
        """Picks up a random question"""
        if ctx.author.top_role not in self.allowed_roles:
            await ctx.send("Sorry but you don't have permission to do that :/")
            return

        if not self.is_qa_running:
            await ctx.send("Ey! there isn't a Q&A session yet")
            return

        if len(self.questions) > 0:
            question = self.questions.pop(random.randint(0, len(self.questions)-1))
            await ctx.send(
                embed=discord.Embed(
                    color=0x301baa,
                    title=f"From {question['from'].name}",
                    description=question['question']
                )
            )

        else:
            await ctx.send("No questions left!")


def setup(bot):
    bot.add_cog(Qa(bot))
