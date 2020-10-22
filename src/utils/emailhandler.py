from discord import Embed
from asyncio import sleep
from re import findall
from re import sub
import imaplib
import email

emaildata = open("EMAIL_LOGIN").read().splitlines()

imap = imaplib.IMAP4_SSL(emaildata[0])
imap.login(emaildata[1], emaildata[2])

init_status, init_messages = imap.select("INBOX")

async def start(emailchannel):
    global init_status, init_messages
    while True:
        messages = imap.select("INBOX")[1]
        if int(messages[0]) > int(init_messages[0]):
            msg = str(email.message_from_bytes(imap.fetch(messages[0].decode(), "(RFC822)")[1][0][1]))
            embed = Embed(
                title=findall(r'From: .*', msg)[0],
                description=findall(r'Subject: .*', msg)[0]
            )
            content = sub(
                r'--[\w]*\nContent-Type: text\/html[\S\s]*', '',
                findall(r'(?<=Content-Type: text\/plain; charset="UTF-8"\n)[\S\s]*(?=--000000000000)', msg)[0])
            if content != '':
                embed.add_field(name="Content:", value=content)

            await emailchannel.send(embed=embed)
            init_messages = messages

        await sleep(5)