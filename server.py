import redis
from flask_sock import Sock
import time
import json
from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template
from jproperties import Properties
import os

global app

configs = Properties()
with open('./config/app-config.properties', 'rb') as config_file:
    configs.load(config_file)
r = redis.Redis(host=os.getenv('HOST', "localhost"),
                port=os.getenv('PORT', 6379),
                password=os.getenv('PASSWORD', "admin"),
                decode_responses=True)
app = Flask(__name__)
sock = Sock(app)
location = os.getenv('LOCATION', "A")


@app.route('/new-player')
def newplayer():
    return render_template('add-player.html')

@app.route('/add-player',methods = ['POST'])
def adduser():
    pname = request.form['playerName']
    age = request.form['age']
    username = request.form['username']
    profile = {"name": pname, "username": username, "age": age, "location": location}
    r.json().set("player:" + username, "$", profile)
    return redirect(url_for('overview', username=username))

@app.route('/')
def overview():
    username = request.args.get('username')
    profile = r.json().get("player:" + username)
    return render_template('overview.html', username=username)


@sock.route('/player/<username>')
def price(sock, username):
    print(username)
    profile = r.json().get("player:" + username)
    name = ''
    location = ''
    score = ''
    while True:
        data = json.dumps(
            {"name": name, "username": username, "location": location, "score": score})
        sock.send(data)
        time.sleep(3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5555)
