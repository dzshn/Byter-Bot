import discord, ka, requests
from os import environ
class byterbot(discord.Client):
	async def on_ready(self):
		ka.status = "online"
		print("[Bot - Info]: > Ready")
		print("[Bot - Info]: > logged in as %s" % self.user)

	async def on_message(self,m):
		if m.content.startswith('%'):
			ctx = m.content[1:].split(' ')
			cm = ctx[0]
			if cm == "t":
				#await m.delete()
				await m.channel.send('Bot online')

			elif cm == "dcnt" and m.author.id == 310449948011528192:
				await m.channel.send('Shutting down...')
				await self.close()

			else: await m.channel.send(cm+": command not found")

		elif ("good night", "goodnight", "gn",) in m.content: await m.add_reaction("♥")

		elif m.author.name == "PriVer" and "good night" in m.content or "goodnight" in m.content: await m.channel.send("Good night Pri!")
			
		elif self.user in m.mentions: await m.channel.send('Hey, my prefix here is %')

ka.ka()
ka.status = "starting"
bot = byterbot()
bot.run(environ["TKN"])
