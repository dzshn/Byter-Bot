import discord
from fuzzywuzzy.process import extractOne
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(color=0xfa0505, title=":x: Error!")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.message.add_reaction('❗')

        elif isinstance(error, commands.CommandNotFound):
            command = ctx.message.content.split()[0][len(ctx.prefix):]
            suggestion = extractOne(command, self.bot.commands)[0]
            embed.description = f"Command {command} not found, did you mean {suggestion}?"

        elif isinstance(error, commands.NotOwner):
            embed.description = "Sorry but this command can only be issued by the bot owner"

        elif isinstance(error, commands.CheckFailure):
            embed.description = f"An check error occurred: {error}"

        elif isinstance(error, commands.UserInputError):
            embed.description = str(error)

        elif isinstance(error, discord.Forbidden):
            embed.description = "An permission error occured"

        else:
            embed.description = (
                "An unknown error occurred!\n\n"
                "This has been anonimously[[0]](https://docs.byterbot.com/#extras.error_data) reported to my dev, please consider opening an issue [on my server](https://discord.gg/h4sFrNj)\n\n"
                f"**Error is:** {error}"
            )

            await self.bot.get_channel(741024906774577201).send(
                f"<@{self.bot.owner_id}>",
                embed=discord.Embed(
                    color=0xfa0505,
                    title="**Error!**",
                    description=(
                        f"**On command :** {ctx.command}\n"
                        f"**Message content :** {ctx.message.content}\n"
                        f"**Error :** {error}\n"
                    )
                )
            )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
