from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from dice import HumanPlayer, AIPlayer, Game
import time

app = Flask(__name__)
CORS(app)

games = {}

@app.route('/')
# 定义一个名为index的函数
def index():
    # 返回一个名为index.html的模板
    return render_template('index.html')

@app.route('/play', methods=['GET'])
# 定义一个名为play的函数
def play():
    name = request.args.get('name')
    player1 = HumanPlayer(name)
    player2 = AIPlayer('AIplayer')
    game = Game(player1, player2)
    games[name] = game
    # 返回一个名为play.html的模板
    return render_template('play.html')

@app.route('/roll', methods=['GET'])
# 定义一个roll函数，用于模拟掷骰子
def roll():
    name = request.args.get('name')
    return games[name].player_roll()

@app.route('/select', methods=['POST'])
@cross_origin()
def select():
    name = request.args.get('name')
    selected = request.json['selected']
    return games[name].player_select(selected)

@app.route('/stop', methods=['POST'])
@cross_origin()
def stop():
    name = request.args.get('name')
    selected = request.json['selected']
    return games[name].player_select_stop(selected)
    
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')