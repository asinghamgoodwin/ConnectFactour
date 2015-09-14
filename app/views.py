from flask import render_template, flash, redirect
from app import app
from connectFactour import *
# from .forms import coinMoveForm

gamer1 = gamer('X')
gamer2 = gamer('O')
newGame = game(gamer1, gamer2)

@app.route('/')
@app.route('/index')
# @app.route('/kitties')
def index():
#    form = coinMoveForm()
#    gamer1 = gamer('X')
 #   gamer2 = gamer('O')
   # newGame = game(gamer1, gamer2)
    if form.validate_on_submit():
        flash('coin1 moved to: "%s", coin2 moved to: "%s"' % 
                (form.coin1.data, form.coin2.data))
        print (form.coin1.data, form.coin2.data)
        return redirect('/kitties')
    return render_template('index.html',
                            title='Connect Factour!',
                            game=newGame)
#                            form=form)

#@app.route('/index/<toBeParsed>', methods=['GET'])
@app.route('/index?coin1=<newCoin1>&coin2=<newCoin2>')
def getFormData(newCoin1, newCoin2):
    print "getFormData got called"
#    newCoin1 = toBeParsed[-9]
#    newCoin2 = toBeParsed[-1]
    product = newCoin1*newCoin2
    print product
    for y in range(6):
        for x in range(6):
            if newGame.grid[y][x].number == product:
                newGame.grid[y][x].take(gamer1)
                print "made move"

    return render_template('index.html',
                            title='Connect Factour!',
                            game=newGame) 






