import discord, ka
from secrets import choice
from os import environ

class byterbot(discord.Client):
    reDb = {}

    async def on_ready(self):
        ka.status = "online"
        print("[Bot - Main]: Ready")
        print("[Bot - Info]: (i) logged in as %s" % self.user)
        print("[Bot - Info]: (l) loading reaction database")
        async for i in self.get_channel(740539699134857337).history():
            if i.content in self.reDb:
                self.reDb[i.content].append(i.attachments[0].url)
            else:
                self.reDb[i.content] = [i.attachments[0].url]

        print("[Bot - Info]: (l) loaded %s categories" % len(self.reDb))

    async def on_message(self, m):
        if m.content.startswith('%'):
            ctx = m.content[1:].split(' ')
            cm = ctx[0]
            if cm == "t":
                await m.channel.send('Bot online')

            elif cm == "dcnt" and m.author.id == 310449948011528192:
                await m.channel.send('Shutting down...')
                await self.close()

            elif cm in self.reDb:
                await m.channel.send(choice(self.reDb[cm]))

            else:
                await m.channel.send(cm + ": command not found")

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]				
            print("[Bot - Info]: (l) new gif detected, added to db, now %s gifs loaded" % len(self.reDb))

        elif m.content.startswith('request:'):
            await m.add_reaction("⬆")
            await m.add_reaction("⬇")

        elif "good night" in m.content.lower() or "goodnight" in m.content.lower() or "gn" in m.content.lower():
            await m.add_reaction("❤️")

        elif m.author.id == 724720098077573202 and "good night" in m.content.lower() or "goodnight" in m.content.lower():
            await m.channel.send("Good night Pri!")

        elif self.user in m.mentions:
            await m.channel.send('Hey!')


ka.ka()
ka.status = "starting"
bot = byterbot()
bot.run(environ["TKN"])
