from pathlib import Path

import aiohttp
import discord
from discord.ext import commands

import config


class ByterBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(*config.prefixes),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
            intents=discord.Intents(guild_messages=True, guilds=True, reactions=True)
        )

        self.add_check(self.global_check)
        self.config = config
        self.session = None
        for i in Path("exts").glob("*.py"):
            if not i.name.startswith('_'):
                try:
                    self.load_extension(str(i)[:-3].replace('/', '.'))

                except commands.ExtensionError:
                    pass

    async def global_check(self, ctx):
        perms = ctx.channel.permissions_for(ctx.me)
        if perms.send_messages and perms.embed_links:
            return True

        raise commands.BotMissingPermissions

    async def on_ready(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_disconnect(self):
        self.session.close()


bot = ByterBot()
bot.run(open("TOKEN").read())
