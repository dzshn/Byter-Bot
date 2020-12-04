import asyncio

import discord
from discord.ext import commands
from googletrans import Translator as GTr


class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = GTr()
        self.auto_translate_chat = self.bot.get_channel(745400744303394917)

    @commands.command(aliases=["tr"])
    async def translate(self, ctx, *, text: commands.clean_content):
        """
        Translates given text on Google Translate

        Use !! for translating last message in chat
        """
        if text == "!!":
            to_tr = await ctx.channel.history(limit=2).flatten()
            to_tr = to_tr[-1].content

        else:
            to_tr = text

        async with ctx.channel.typing():
            # https://github.com/ssut/py-googletrans/issues/234
            for _ in range(10):
                try:
                    translation = await self.bot.loop.run_in_executor(None, self.translator.translate, text)

                except AttributeError:
                    await asyncio.sleep(5)

                else:
                    embed = discord.Embed(
                        title=f"Translation (detected {translation.src})",
                        description=translation.text
                    )
                    embed.set_footer(text="Powered by Google Translate")
                    await ctx.send(embed=embed)
                    return

            await ctx.send("Could not translate after 10 tries")


def setup(bot):
    bot.add_cog(Translator(bot))
