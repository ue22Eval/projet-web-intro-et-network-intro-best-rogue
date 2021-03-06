from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game, player
from time import time
import json

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()
play = player.Player(chr(0x1F471))




@app.route("/")
def index():
    map = game.getMap()
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), money= play._money, life = play._life)

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    m1, m2 = game.move(dx,dy, 0)
    data, ret = m1[0], m1[1]
    data2, ret2 = m2[0], m2[1]

    if ret:
        socketio.emit("response", data)
    if ret2:
        socketio.emit("responseM", data2)
    if len(data) == 1:  #cas de la victoire
        if data[0] == True: 
            socketio.emit("victory", data)
            
@socketio.on("move2")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move2 ws message")
    dx = json['dx']
    dy = json["dy"]

    m1, m2 = game.move(dx,dy, 1)
    data, ret = m1[0], m1[1]
    data2, ret2 = m2[0], m2[1]

    if ret:
        socketio.emit("response2", data)
    if ret2:
        socketio.emit("responseM", data2)
    if len(data) == 1:  #cas de la victoire
        if data[0] == True: 
            socketio.emit("victory", data)

if __name__=="__main__":
    socketio.run(app, port=5001)