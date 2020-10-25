from . import admin, api, minigame, other
from ..utils import errors

async def parse_command(m, c):
    con = m.content[1:] if m.content.startswith('%') else m.content[2:]
    ctx = con.split(' ')
    cm = ctx[0]
    if cm in c.reDb:
        await m.channel.send(c.reDb[cm])
        return

    cmds = {
        'eval': {
            'func': admin.bot_eval,
            'args': [c, '\n'.join(con[5:].strip('\n').split('\n')[1:-1])]
        },
        'restart': {
            'func': admin.restart,
            'args': [c, con[8:] if len(ctx)>1 else ""]
        },
        'api avatar': {
            'func': api.avatar,
            'args': [con[11:] if len(ctx)>2 else None]
        },
        'api cat': api.cat,
        'api dog': api.dog,
        'api fox': api.fox,
        'api joke': api.joke,
        'api name': {
            'func': api.name,
            'args': [con[9:] if len(ctx)>2 else None]
        },
        'api qr': {
            'func': api.qr,
            'args': [con[7:] if len(ctx)>2 else None]
        },
        'api time': {
            'func': api.time,
            'args': [ctx[2:] if len(ctx)>2 else None]
        },
        'api wiki': {
            'func': api.wiki,
            'args': [con[9:] if len(ctx)>2 else None]
        },
        'api xkcd': {
            'func': api.xkcd,
            'args': [con[9:] if len(ctx)>2 else None]
        },
        'avatar': {
            'func': api.avatar,
            'args': [con[7:] if len(ctx)>1 else None]
        },
        'cat': api.cat,
        'dog': api.dog,
        'fox': api.fox,
        'joke': api.joke,
        'name': {
            'func': api.name,
            'args': [con[5:] if len(ctx)>1 else None]
        },
        'qr': {
            'func': api.qr,
            'args': [con[7:] if len(ctx)>1 else None]
        },
        'time': {
            'func': api.time,
            'args': [ctx[1:] if len(ctx)>1 else None]
        },
        'wiki': {
            'func': api.wiki,
            'args': [con[5:] if len(ctx)>1 else None]
        },
        'xkcd': {
            'func': api.xkcd,
            'args': [con[5:] if len(ctx)>1 else None]
        },
        'minigame 2048': {
            'func': minigame.game2048,
            'args': [c]
        },
        'minigame tictactoe': {
            'func': minigame.tictactoe,
            'args': [c]
        },
        'minigame simon': {
            'func': minigame.simon,
            'args': [c]
        },
        'embed': {
            'func': other.embed,
            'args': [con[6:]]
        },
        'gifs': {
            'func': other.gifs,
            'args': [c]
        },
        'help': {
            'func': other.helpb,
            'args': [con[5:]]
        },
        'info': {
            'func': other.info,
            'args': [con[5:]]
        },
        'poll': {
            'func': other.poll,
            'args': [con[5:]]
        },
        'stats': {
            'func': other.stats,
            'args': [c]
        },
        '8ball': {
            'func': other.ball8,
            'args': [c]
        },
    }

    for i in cmds.keys():
        if con.startswith(i):
            if isinstance(cmds[i], dict):
                if None in cmds[i]['args']:
                    raise errors.CommandError("Missing arguments")

                await cmds[i]['func'](m, *cmds[i]['args'])

            else:
                await cmds[i](m)

            return

    await m.channel.send('command not found')