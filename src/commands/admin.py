import traceback
from contextlib import redirect_stdout
from functools import wraps
from io import StringIO

import discord

from ..utils import utils


def check(m, c):
    if m.author == c.get_user(310449948011528192):
        return True

    else:
        raise Exception("User doesn't have permission to run command")

async def bot_eval(m, c, con):
    if not check(m, c):
        return

    try:
        eval_stdout = StringIO()
        with redirect_stdout(eval_stdout):
            exec(con, {"message": m, "client": c})

        out = eval_stdout.getvalue()
        out = out.replace('`', "'")
        if len(out) > 2000:
            out = out[:2000]+'\n[...]'

        await m.channel.send(
            embed=discord.Embed(
                color=0x05ba05,
                title="Code Evaluated with success :white_check_mark:",
                description="**Output :** ```py\n%s```" % out
        ))

    except:
        await m.channel.send(
            embed=discord.Embed(
                color=0xfa0505,
                title="Error!",
                description="**Output:** ```py\n%s```\n**Traceback :** ```py\n%s```" % (out[:1000], traceback.format_exc()[:1000])
        ))

async def restart(m, c, arg):
    if not check(m, c):
        return

    if arg.lower() == "now":
        await m.channel.send(
            embed=discord.Embed(
                title="Rebooting **now**"
        ))
        await utils.bot_reload(c, update=False, delay=False)
    
    else:
        await m.channel.send(
            embed=discord.Embed(
                title="Rebooting in a minute!"
        ))
        await utils.bot_reload(c, update=False)
