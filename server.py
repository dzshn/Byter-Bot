from flask import Flask, request
from os import system

app = Flask("")

@app.route('/')
def index():
    return "why are you here? how did you get my ip? this is for webhooks, get out"

@app.route('/webhook', methods=["POST", "GET"])
def whook():
    if request.method == "POST":
        if "commits" in request.json:
            system("git pull")
            
        return '', 200

    else:
        return "yo, use a post request"

def start():
    app.run(host="0.0.0.0", port=80)