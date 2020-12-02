from discord.ext import commands

class Db:
    def __init__(self):
        self.reaction_db = {}
        self.ball8_db = {}

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.database = Db()

    @commands.Cog.listener()
    async def on_ready(self):
        async for i in self.bot.get_channel(740539699134857337).history():
            if i.content in self.bot.database.reaction_db:
                self.bot.database.reaction_db[i.content].append(i.attachments[0].url)

            else:
                self.bot.database.reaction_db[i.content] = [i.attachments[0].url]

        async for i in self.bot.get_channel(742479941504860341).history():
            self.bot.database.ball8_db[i.content] = i.attachments[0].url


def setup(bot):
    bot.add_cog(Database(bot))
