import redis
from flask_sock import Sock
import time
import json
from flask import Flask, redirect, url_for, request, render_template
from jproperties import Properties
import os
import threading
import random

global app

configs = Properties()
with open('./config/app-config.properties', 'rb') as config_file:
    configs.load(config_file)


def playGame(stock):
    endTime = time.time() + 60 * 15
    # Game will run for 15 min
    while time.time() < endTime:
        players = r.smembers("game:1")
        for player in players:
            generatedScore = random.randint(1, 1000)
            r.zadd("leaderboard", {player: generatedScore})
            time.sleep(1)


if __name__ == '__main__':
    r = redis.Redis(host=os.getenv('HOST', "localhost"),
                    port=os.getenv('PORT', 6379),
                    password=os.getenv('PASSWORD', "admin"),
                    decode_responses=True)
    app = Flask(__name__)
    sock = Sock(app)
    location = os.getenv('LOCATION', "A")
    t = threading.Thread(target=playGame, args=(location))
    t.start()


@app.route('/')
def newplayer():
    return render_template('add-player.html', location=location)

@app.route('/add-player',methods = ['POST'])
def adduser():
    pname = request.form['playerName']
    age = request.form['age']
    username = request.form['username']
    profile = {"name": pname, "username": username, "age": age, "location": location}
    r.hmset("player:" + username, profile)
    r.sadd("game:1", "player:" + username)
    return redirect(url_for('overview', username=username, location=location))

@app.route('/overview')
def overview():
    username = request.args.get('username')
    if username is None:
        username = ''
    return render_template('overview.html', username=username, location=location)

@app.route('/profile')
def profile():
    username = request.args.get('username')
    if username is None:
        username = ''
    profile = r.hgetall("player:" + username)
    name = profile['name']
    location = profile['location']
    age = profile['age']
    return render_template('profile.html', username=username, location=location, age=age, name=name)


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', location=location)


@sock.route('/player/<username>')
def playerMetadata(sock, username):
    print(username)
    profile = r.hgetall("player:" + username)
    name = profile['name']
    location = profile['location']
    while True:
        score = r.zscore("leaderboard", "player:" + username)
        data = json.dumps(
            {"name": name, "username": username, "location": location, "score": score})
        sock.send(data)
        time.sleep(3)

@sock.route('/players')
def getActivePlayers(sock):
    while True:
        players = r.sscan("game:1", cursor=0, count=2)
        cur = players[0]
        playerList = players[1]
        while cur != 0:
            for p in playerList:
                profile = r.hgetall(p)
                data = json.dumps({"username": profile['username'], "location": profile['location']})
                sock.send(data)
            players = r.sscan("game:1", cursor=cur, count=2)
            cur = players[0]
            playerList = players[1]

        if cur == 0 and len(playerList) > 0:
            for p in playerList:
                profile = r.hgetall(p)
                data = json.dumps({"username": profile['username'], "location": profile['location']})
                sock.send(data)
        time.sleep(10)
        sock.send(json.dumps({"_NODATA": "_NODATA"}))


@sock.route('/game/01/leaderboard')
def getLeaderboard(sock):
    while True:
        lb = r.zrange("leaderboard", start=0, end=9, desc=True, withscores=True)
        i = 0
        while i < len(lb):
            val = list(lb[i])
            data = json.dumps({"player": val[0], "score": val[1]})
            sock.send(data)
            i += 1
        time.sleep(5)
        sock.send(json.dumps({"_NODATA": "_NODATA"}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5555)
