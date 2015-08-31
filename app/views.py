from flask import render_template
from app import app
import connectFactour

@app.route('/')
@app.route('/index')
@app.route('/kitties')
def index():
    #gamer = {"letter":"O"}
    gamer1 = gamer('X')
    gamer2 = gamer('O')
    newGame = game(gamer1, gamer2)
    return render_template('index.html',
                            title='Connect Factour!',
                            game=newGame)








