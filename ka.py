from flask import Flask
from threading import Thread
a = Flask('')
status = "offline"
@a.route('/')
def home():
	return '''
	<title>Bot status</title>
	<style>html{background-color:#00002a; color: #a0a0b0; font-family: Arial; text-align: center; font-size: xx-large; width: 800; margin: 0 auto}</style>
	<h1>The bot is %s </h1>
	''' % status

def run(): a.run(host='0.0.0.0',port=8080)
def ka():  
    t = Thread(target=run)
    t.start()