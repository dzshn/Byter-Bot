from secrets import choice
from os import environ
from time import time
import discord
import ka

initTime = time()

class byterbot(discord.Client):
    reDb = {}
    readyTime = 0
    loadTime = 0

    async def on_ready(self):
        self.readyTime = time()
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
        self.loadTime = time()

    async def on_message(self, m):
        if m.content.startswith(('%', 'b!')):
            ctx = m.content[1:].split(' ') if m.content.startswith('%') else m.content[2:].split(' ')
            cm = ctx[0]

            if cm == "help":
                embed=discord.Embed(color=0x301baa)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/741457274530299954/741457798705184830/BUTTON_byter.webp")
                embed.add_field(name="Hello! here are the valid commands",
                                value='''
                                        **help** - show this info
                                        **gifs** - lists all loaded categories of gifs/images
                                        **stats** - shows some useful stats
                                        **poll title, *options ** - makes a poll, options may be none (yes/no) or phrases separated by a comma (up to 20), title may also be omitted if there arent other arguments
                                      ''',
                                inline=False)
                embed.add_field(name="And functions",
                                value='''
                                        **gifs / images !** - use the command %gifs to see what categories are avaiable and use % plus the name for me to pick a gif/image for you!
                                      ''',
                                inline=False)
                embed.set_footer(text="creucat.com © PriVer - bot developed by leninnog",
                                 icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                await m.channel.send('', embed=embed)

            elif cm == "info":
                if ctx[1] in ["character", "char"]:
                    if len(ctx) == 2:
                        embed = discord.Embed(color=0x00002a)
                        embed.add_field(name="Characters!",
                                        value='''
                                                Want to know about the créu characters? this is the way to go!

                                                Just put the name of the character you want to know in front of this command! they are Créu, Petita, Liu-Liu, Muji, Printy, Mek & Krek, Rona & mou and of course me!
                                              ''',
                                        inline=False)
                        embed.set_thumbnail(url=choice(["https://cdn.discordapp.com/attachments/741457274530299954/741615794340888586/selocreu2.gif", "https://cdn.discordapp.com/attachments/741457274530299954/741616136134852678/selocreu1.gif"]))
                        embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                         icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")
                        await m.channel.send('', embed=embed)
                        return 1

                    elif ctx[2].lower() in ["creu", "créu"]:
                        color = 0xf2f4f5
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741460429733101678/BUTTON_creu.webp"
                        name = "Créu"
                        desc = "While naive and sometimes  clueless, Créu is a friend for life and brings joy to everyone he meets! A little out of touch with reality, Créu enjoys the world of the wide Web. Has a crush on Petita and loves to dance!"
                        favs = "<:coffee:741469635492446268> Latte\n\n<:ice_cream:741469513773613118> Coconut\n\n<:music:741469877143076946> Funk"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741460469960802424/CHARCREUcreu.webp"

                    elif ctx[2].lower() == "petita":
                        color = 0x0a0201
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741476662469984316/BUTTON_petita.webp"
                        name = "Petita"
                        desc = "Petita loves a little friendly competition! and can be a little jealous of Créu sometimes. She will speak up for what’s right and never gives up!"
                        favs = "<:coffee:741469635492446268> Brewed, no cream\n\n<:ice_cream:741469513773613118> Strawberry Vanilla\n\n<:music:741469877143076946> Pop, Samba"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741476770276048986/CHARCREUpetita.webp"

                    elif ctx[2].lower() in ["liu-liu", "liuliu"]:
                        color = 0xe6e4e5
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741479280831103076/BUTTON_liuliu.webp"
                        name = "Liu-Liu"
                        desc = "Liu-Liu loves great food and dreams of becoming a famous chef someday. Usually doesn’t care what anyone says. Always down for ice cream and coffee!"
                        favs = "<:coffee:741469635492446268> Cappuccino\n\n<:ice_cream:741469513773613118> Cookie Dough\n\n<:music:741469877143076946> Swing"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741479323999141978/CHARCREUliuliu.webp"

                    elif ctx[2].lower() == "muji":
                        color = 0xe8a2a5
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741480701693788200/BUTTON_muji.webp"
                        name = "Muji"
                        desc = "Muji is Créu's cousin who lives abroad. She runs a beauty vlog and loves the world of social media. She believes change is beautiful! As someone who enjoys philosophy and reading, she may get upset when others judge her by her looks."
                        favs = "<:coffee:741469635492446268> Caramel Macchiato\n\n<:ice_cream:741469513773613118> Red Velvet\n\n<:music:741469877143076946> Rock n' Roll"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741480741413584946/CHARCREUmuji.webp"

                    elif ctx[2].lower() == "printy":
                        color = 0x0afe0b
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741481764589142046/BUTTON_printy.webp"
                        name = "Printy"
                        desc = "Petita's little sister. Even though she's the youngest of the group, Printy's got a keen interest on vintage artifacts, especially from the 90’s and 2000’s. Always curious and wanting to learn and discover. She absolutely loves Pixel art!"
                        favs = "<:coffee:741469635492446268> Frappe\n\n<:ice_cream:741469513773613118> Tutti Frutti Popsicle\n\n<:music:741469877143076946> Video Game Music"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741481809262542928/CHARCREUprinty.webp"

                    elif ctx[2].lower() in ["mek", "krek", "mek&krek"]:
                        color = 0x0a0b0c
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741483630534328351/BUTTON_mekrek.webp"
                        name = "Mek & Krek"
                        desc = "Like two rival corporations, these two are inseparable but tend to fight a lot. They often find that the thing one accuses the other of doing is exactly what they're guilty of."
                        favs = "<:coffee:741469635492446268> Espresso / Americano\n\n<:ice_cream:741469513773613118> Green tea Mochi / Mint Dippin Dots\n\n<:music:741469877143076946> Dubstep / Classical"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741483723740151868/CHARCREUmekkrek.webp"

                    elif ctx[2].lower() == "byter":
                        color = 0x301baa
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741457798705184830/BUTTON_byter.webp"
                        name = "Byter"
                        desc = "Byter is a tiny hero who lives inside your computer. He makes sure no malware gets through and despises spam! Many have heard of him but never truly seen him."
                        favs = "<:coffee:741469635492446268> ?\n\n<:ice_cream:741469513773613118> ?\n\n<:music:741469877143076946> Eletronic"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741460380710207588/CHARCREUbyter.webp"

                    elif ctx[2].lower() in ["rona", "mou", "rona&mou"]:
                        color = 0xeaeced
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741486168578981888/BUTTON_ronamou.webp"
                        name = "Rona & Mou"
                        desc = "Créu's parents! Always eager to help. They make sure the kitties don’t get into too much trouble or mischievousness!"
                        favs = "<:coffee:741469635492446268> Irish Coffee / Bicerin\n\n<:ice_cream:741469513773613118> Butter Pecan / Pistachio\n\n<:music:741469877143076946> Bossa Nova / New Age"
                        imgUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741486251319885824/CHARCREUronamou.webp"

                    else:
                        color = 0xD3D152
                        thumbUrl = "https://cdn.discordapp.com/attachments/741457274530299954/741553915740422204/thonk.png"
                        name="%s: Not found\n" % ctx[2]
                        desc="???"
                        favs="<:coffee:741469635492446268> ???\n\n<:ice_cream:741469513773613118> ???\n\n<:music:741469877143076946> ???"
                        imgUrl="https://cdn.discordapp.com/attachments/741457274530299954/741553915740422204/thonk.png"

                    if ctx[2] != "":
                        embed = discord.Embed(color=color)
                        embed.set_thumbnail(url=thumbUrl)
                        embed.add_field(name=name, value=desc, inline=False)
                        embed.add_field(name="Favorites", value=favs, inline=False)
                        embed.set_image(url=imgUrl)
                        embed.set_footer(text="creucat.com/characters © PriVer - bot developed by leninnog",
                                         icon_url="https://cdn.discordapp.com/attachments/741457274530299954/741457487277850724/creucat.ico.gif")

                await m.channel.send('', embed=embed)

            elif cm == "t":
                await m.channel.send('Bot online')
                print(m.content)

            elif cm == "gifs":
                embed = discord.Embed(color=0x301baa)
                embed.add_field(name="Hey, there are %s categories loaded" % len(self.reDb),
                                value="**categories:** %s\n\nyou may use the categories as a command, and I'll pick an image/gif from there!" % str(self.reDb.keys())[10:].strip("()[]").replace("'", ''),
                                inline=False)
                await m.channel.send('', embed=embed)

            elif cm == "stats":
                embed = discord.Embed(color=0x301baa)
                embed.add_field(name="Here are some time metrics",
                                value='''
                                        **uptime**: I'm online for %s seconds
                                        **ready time**: I took %s seconds to connect to discord
                                        **load time**: I took %s seconds to load after connecting
                                      ''' % (round(time()-initTime, 2), round(self.readyTime-initTime, 2), round(self.loadTime-self.readyTime, 2)),
                                inline=False)
                await m.channel.send('', embed=embed)

            elif cm == "poll":    
                embed = discord.Embed(color=0xb20ac5)
                options = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷' ,'🇸', '🇹']
                poll = m.content.replace('b!', '%')[5:].split(',')
                if len(ctx) == 1:
                    poll[0] = 'poll'
                pollText = ''
                for i in poll[1:]:
                    pollText += options[poll[1:].index(i)]+' '+i+'\n'
                if len(poll) == 1:
                    pollText = '✅ / ❎'
                embed.add_field(name=poll[0].strip().title(),
                                value=pollText)
                pollMsg = await m.channel.send('', embed=embed)
                for i in range(len(poll[1:])):
                    await pollMsg.add_reaction(options[i])
                if len(poll) == 1:
                    await pollMsg.add_reaction('✅')
                    await pollMsg.add_reaction('❎')

            elif cm in self.reDb:
                await m.channel.send(choice(self.reDb[cm]))

            else:
                await m.channel.send(cm + ": command not found")

        elif m.channel.id == 740539699134857337:
            if m.content in self.reDb:
                self.reDb[m.content].append(m.attachments[0].url)
            else:
                self.reDb[m.content] = [m.attachments[0].url]
            print("[Bot - Info]: (l) new gif detected, added to db, now %s categories loaded" % len(self.reDb))

        elif "virus" in m.content.lower():
            await m.add_reaction(self.get_emoji(726611950200553502))

        elif "good night" in m.content.lower() or "goodnight" in m.content.lower():
            await m.add_reaction("❤️")


ka.ka()
ka.status = "starting"
bot = byterbot()
bot.run(environ["TKN"])