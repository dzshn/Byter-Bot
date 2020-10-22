import discord

from ..utils import utils

async def restart(m, c):
    if m.author == c.get_user(310449948011528192):
        await m.channel.send(
            embed=discord.Embed(
                title="Rebooting in a minute!"
           )
        )
        await utils.bot_reload(c, update=False)

    else:
        await m.channel.send(
            embed=discord.Embed(
                title="Error!",
                description="This command can only be issued by my owner"
            )
        )