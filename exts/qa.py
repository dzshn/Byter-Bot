import random
from io import BytesIO

import discord
from discord.ext import commands


class Qa(commands.Cog, command_attrs={'hidden': True}):
    def __init__(self, bot):
        self.bot = bot
        self.is_qa_running = False
        self.creu_guild_id = 725421276562325514
        self.allowed_role_ids = [
            728875097808699473,
            777720322446983179,
            726615159459676180
        ]
        self.questions = None

    @commands.group()
    async def qa(self, ctx):
        """Commands used for an Q&A event"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Missing or invalid subcommand")

    @qa.command(name="start")
    @commands.is_owner()
    async def qa_start(self, ctx):
        """Starts up the Q&A session"""
        self.questions = []
        self.is_qa_running = True
        await ctx.send("All set!")

    @qa.command(name="stop")
    @commands.is_owner()
    async def qa_stop(self, ctx):
        """Stops the Q&A session"""
        self.is_qa_running = False
        self.questions = None
        await ctx.send("All clear!")

    @qa.command(name="ask")
    async def qa_ask(self, ctx, *, question):
        """Ask a question, which later be picked at random"""
        if self.is_qa_running:
            self.questions.append({"a": ctx.author, "q": question})
            await ctx.message.add_reaction(
                self.bot.get_emoji(757023230073634922)
            )

        else:
            await ctx.send("Ey! there isn't a Q&A session yet")

    @qa.command(name="pick")
    async def qa_pick(self, ctx):
        """Picks up a random question"""
        if ctx.author.top_role.id not in self.allowed_role_ids:
            await ctx.send("Sorry but you don't have permission to do that :/")
            return

        if not self.is_qa_running:
            await ctx.send("Ey! there isn't a Q&A session yet")
            return

        if len(self.questions) > 0:
            q_obj = self.questions.pop(random.randint(0, len(self.questions)-1))
            await ctx.send(
                embed=discord.Embed(
                    color=0x301baa,
                    description=q_obj['q']
                ).set_author(
                    name=f"{q_obj['a']} ({q_obj['a'].id})",
                    icon_url=q_obj['a'].avatar_url
                )
            )

        else:
            await ctx.send("No questions left!")


def setup(bot):
    bot.add_cog(Qa(bot))
