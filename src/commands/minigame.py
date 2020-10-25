import asyncio
from secrets import choice

import discord
import numpy as np


async def game2048(m, c):
    gameDat = np.array([[0 for i in range(4)] for ii in range(4)])
    gameScr = 0
    gameDat.flat[choice([i for i, j in enumerate(gameDat.flatten()) if j == 0])] = choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
    gameDsp = lambda : '\n'.join([''.join([c.jsonfiles['ming']['2048']['tiles'][n] for n in gameDat[i]]) for i in range(4)])
    gameEmb = discord.Embed()
    gameEmb.add_field(name="2048!", value=gameDsp())
    gameEmb.add_field(name="Score", value=gameScr)
    gEmbUpd = lambda : (gameEmb.set_field_at(0, name="2048!", value=gameDsp()), gameEmb.set_field_at(1, name="Score", value=gameScr))
    gameMsg = await m.channel.send(embed=gameEmb)

    for i in ['⬆️', '⬇️', '⬅️', '➡️']:
        await gameMsg.add_reaction(i)

    while 0 in gameDat:
        try:
            r, u = await c.wait_for("reaction_add", check=lambda r, u: str(r.emoji) in ['⬆️', '⬇️', '⬅️', '➡️'] and r.message.id == gameMsg.id and u == m.author, timeout=120)

        except asyncio.TimeoutError:
            await m.channel.send('× -× timed out')

        if m.guild.me.permissions_in(m.channel).manage_messages:
            await r.remove(u)

        def move(gdat, gscr, ay, ax, r1=0, r2=4, r3=0, r4=4):
            for _ in range(4):
                for iy in range(r1, r2):
                    for ix in range(r3, r4):
                        if gdat[iy][ix] != 0:
                            if gdat[iy+ay][ix+ax] == 0:
                                gdat[iy+ay][ix+ax] = gdat[iy][ix]
                                gdat[iy][ix] = 0

                            elif gdat[iy+ay][ix+ax] == gdat[iy][ix]:
                                gdat[iy+ay][ix+ax] += 1
                                gdat[iy][ix] = 0
                                gscr += 2**gdat[iy+ay][ix+ax]

            return gdat, gscr

        if str(r.emoji) == '⬆️':
            gameDat, gameScr = move(gameDat, gameScr, -1, 0, r1=1)

        elif str(r.emoji) == '⬇️':
            gameDat, gameScr = move(gameDat, gameScr, 1,  0, r2=3)

        elif str(r.emoji) == '⬅️':
            gameDat, gameScr = move(gameDat, gameScr, 0, -1, r3=1)

        elif str(r.emoji) == '➡️':
            gameDat, gameScr = move(gameDat, gameScr, 0,  1, r4=3)


        await gameMsg.edit(embed=gameEmb)
        await asyncio.sleep(.05)
        gameDat.flat[choice([i for i, j in enumerate(gameDat.flatten()) if j == 0])] = 1
        gEmbUpd()
        await gameMsg.edit(embed=gameEmb)

    await gameMsg.edit(embed=discord.Embed(title="Game over , -,", description=f"Played by: {m.author.name}\n{gameDsp()}\n**Score:** {gameScr}"))


async def tictactoe(m, c):
    gameMsg = await m.channel.send(embed=discord.Embed(description=f"Waiting for acception, {m.mentions[0].name}, please react with ✅ to accept"))
    await gameMsg.add_reaction('✅')
    try:
        await c.wait_for('reaction_add', check=lambda r, u : str(r.emoji) == '✅' and u == m.mentions[0], timeout=60)

    except asyncio.TimeoutError:
        await gameMsg.edit(embed=discord.Embed(description='Acception timed out'))
        return 1

    crrntPl = choice([1, 2])
    players = [m.author, m.mentions[0]]
    gameDat = np.zeros((3, 3), dtype=int)
    gameDsp = lambda : '\n'.join([''.join(
        [[':white_large_square:', ':x:', ':o:'][n] for n in gameDat[i]]) for i in range(3)]) + ("\n%s's turn" % players[crrntPl-1] if crrntPl != 0 else '')
    gameEmb = discord.Embed()
    gameEmb.add_field(name='Tic-Tac-Toe!', value=gameDsp())
    winCmbs = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    await gameMsg.edit(embed=gameEmb)
    while 0 in gameDat:
        try:
            mm = await c.wait_for('message',
                check=lambda mm: mm.author == players[crrntPl-1] and mm.content in [str(i) for i in range(1, 10)],
                timeout=240)

        except asyncio.TimeoutError:
            await m.channel.send("× -× timed out")
            return 1

        if gameDat.flat[int(mm.content)-1] != 0:
            await m.channel.send("invalid move!")

        else:
            gameDat.flat[int(mm.content)-1] = crrntPl
            crrntPl = 1 if crrntPl == 2 else 2
            if m.guild.me.permissions_in(m.channel).manage_messages:
                await mm.delete()

            if any([all([gameDat.flat[j] == 1 for j in i]) for i in winCmbs]):
                crrntPl = 0
                gameEmb.set_field_at(0, name="Game over", value=gameDsp())
                gameEmb.add_field(name="%s wins!" % players[0].name,
                    value='played by %s and %s' % (players[0].name, players[1].name))

            elif any([all([gameDat.flat[j] == 2 for j in i]) for i in winCmbs]):
                crrntPl = 0
                gameEmb.set_field_at(0, name="Game over", value=gameDsp())
                gameEmb.add_field(name="%s wins!" % players[1].name,
                    value='played by %s and %s' % (players[0].name, players[1].name))

            else:
                gameEmb.set_field_at(0, name="Tic-Tac-Toe!", value=gameDsp())
                await gameMsg.edit(embed=gameEmb)

    gameEmb.set_field_at(0, name="Game over", value=gameDsp())
    gameEmb.add_field(name="Tie!", value=f"played by {players[0].name} and {players[1].name}")
    await gameMsg.edit(embed=gameEmb)


async def simon(m, c):
    sequence = [choice([0, 1, 2, 3])]
    gameDat = [0 for i in range(4)]
    gameDsp = lambda : (
        ':green_square:' if gameDat[0] == 0 else ':white_large_square:'
        ':red_square:' if gameDat[1] == 0 else ':white_large_square:'
        '\n'
        ':yellow_square:' if gameDat[2] == 0 else ':white_large_square:'
        ':blue_square:' if gameDat[3] == 0 else ':white_large_square:'
    )

    gameMsg = await m.channel.send(embed=discord.Embed(title="Simon!", description=gameDsp()))
    [await gameMsg.add_reaction(i) for i in ['🟩', '🟥', '🟨', '🟦']]
    await asyncio.sleep(0.1)
    while True:
        for i in sequence:
            gameDat[i] = 1
            await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()))
            await asyncio.sleep(0.1)
            gameDat[i] = 0
            await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()))
            await asyncio.sleep(0.1)

        await gameMsg.edit(embed=discord.Embed(title="Simon!", description=gameDsp()+'\nYour turn'))

        for i in sequence:
            try:
                r, u = await c.wait_for('reaction_add', check=lambda r, u: u == m.author and str(r.emoji) in ['🟩', '🟥', '🟨', '🟦'], timeout=240)

            except asyncio.TimeoutError:
                await gameMsg.edit(embed=discord.Embed(title="Timed out × -×",
                    description=''.join([[':green_square:', ':red_square:', ':yellow_square:', ':blue_square:'][ii] for ii in sequence])))

            if m.guild.me.permissions_in(m.channel).manage_messages:
                await r.remove(u)

            if str(r.emoji) != ['🟩', '🟥', '🟨', '🟦'][i]:
                await gameMsg.edit(embed=discord.Embed(title="Game over , -,",
                    description=''.join([[':green_square:', ':red_square:', ':yellow_square:', ':blue_square:'][ii] for ii in sequence])))
                return 1

        sequence.append(choice([0, 1, 2, 3]))
        await asyncio.sleep(0.5)
