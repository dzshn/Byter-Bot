from flask import Flask, request

app = Flask("")

@app.route('/')
def index():
    return "why are you here? how did you get my ip? this is for webhooks, get out"

@app.route('/webhook', methods=["POST", "GET"])
def whook():
    if request.method == "POST":
        print(request.json)
        return '', 200
    else:
        return "yo, use a post request"

def start():
    app.run(host="0.0.0.0")