from flask import render_template, flash, redirect
from app import app
from connectFactour import *
from .forms import coinMoveForm

@app.route('/')
@app.route('/index')
@app.route('/kitties')
def index():
    #gamer = {"letter":"O"}
    form = coinMoveForm()
    gamer1 = gamer('X')
    gamer2 = gamer('O')
    newGame = game(gamer1, gamer2)
    return render_template('index.html',
                            title='Connect Factour!',
                            game=newGame,
                            form=form)








