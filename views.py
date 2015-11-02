from flask import Flask, render_template, g, redirect
import sqlite3
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional, EqualTo
from models import *
from connectFactour import *
from contextlib import closing
import random
import string
import json
from moveByMove import itWasMyTurn, isMoveLegal, isGameOver

app = Flask(__name__)
app.config.from_object("config")

defaultGame ={"grid": [
                [ [54,""],[56,""],[63,""],[64,""],[72,""],[81,""] ],
                [ [36,""],[40,""],[42,""],[45,""],[48,""],[49,""] ],
                [ [25,""],[27,""],[28,""],[30,""],[32,""],[35,""] ],
                [ [15,""],[16,""],[18,""],[20,""],[21,""],[24,""] ],
                [ [7,""],[8,""],[9,""],[10,""],[12,""],[14,""] ],
                [ [1,""],[2,""],[3,""],[4,""],[5,""],[6,""] ],
                        ],
            "coin1": 1,
            "coin2": 1,
            "upNext": "X",
            "gameOver": False,
            "winner": ""
            } 

class CoinForm(Form):
    coin1 = RadioField('category',
                    choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                    validators=[Optional()])

    coin2 = RadioField('category',
                    choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                    validators=[Optional()])

class NewGameForm(Form):
    pass

@app.route('/newGame',methods = ["GET","POST"])
def newGame():
    gameURL =''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.digits) for _ in range(8)) 
    myURL = '/index/'+gameURL+'/X'
    partnerURL = '/index/'+gameURL+'/O'
    form = NewGameForm()
    if form.validate_on_submit():
        newGame_state =  defaultGame
        newGame_state["coin1"] = random.randint(1,9)
        newGame_state["coin2"] = random.randint(1,9)
        
        # MAKE A NEW ENTRY INTO THE SQL DATABASE
        db = get_db()
        with db:
            cur = db.cursor()
            cur.execute("insert into Game(game_state,game_url) values (?,?)", [json.dumps(newGame_state),gameURL])
        return redirect(myURL)
    return render_template('newGame.html',
                            partnerURL=partnerURL,
                            form=form)

@app.route('/index/<gameURL>/<player>', methods = ["GET", "POST"])
def index(gameURL, player):
    db = get_db()
    with db:
        cur = db.cursor()
        cur.execute("SELECT game_state FROM Game WHERE game_url = '%s'" % gameURL)
        this_game = json.loads(cur.fetchall()[0][0])

    coin1 = str(this_game['coin1'])
    coin2 = str(this_game['coin2'])
    coinPositionHTMLstring = 'The current positions are: '+coin1+' and '+coin2

    if player == "X":
        otherPlayer = 'O'
    else:
        otherPlayer = 'X'
    # there's no error message yet, but if someone tries to
    # make an illegal move there will be...
    errorMessage=""
    gameOverString = ""

    coinForm = CoinForm()
    if coinForm.validate_on_submit():
        coin1 = int(coinForm.coin1.data)
        coin2 = int(coinForm.coin2.data)

        #this is to weed out a submitted form by the wrong player
        errorMessage="Wait your turn!"
        if itWasMyTurn(this_game["upNext"], player):
            moveWasLegal, errorMessage = isMoveLegal(this_game, (coin1, coin2))
            if moveWasLegal:

                product = coin1*coin2
                for r, row in enumerate(this_game["grid"]):
                    for c, cell in enumerate(row):
                        if int(cell[0]) == product:
                            cell[1] = player
                this_game['coin1'] = coin1
                this_game['coin2'] = coin2
                this_game["upNext"] = otherPlayer

                gameIsOver, winner = isGameOver(this_game)
                if gameIsOver:
                    gameOverString = "GAME OVER! PLAYER "+winner+" WINS!"
                    this_game["upNext"] = ""
                    this_game["winner"] = winner
                    this_game["gameOver"] = gameIsOver

                updated_game = json.dumps(this_game)

                db = get_db()
                with db:
                    cur = db.cursor()
                    cur.execute("UPDATE Game SET game_state = '%s' WHERE game_url = '%s'" % (updated_game, gameURL))

    if this_game['upNext'] == player:
        whoseTurnString = "It's your turn!"
    else:
        whoseTurnString = "It's your partner's turn!"


    return render_template('index.html',
                            title='Connect Factour!',
                            form=coinForm,
                            grid = this_game["grid"],
                            gameURL=gameURL,
                            otherPlayer=otherPlayer,
                            myLetter=player,
                            coinPositionHTMLstring=coinPositionHTMLstring,
                            whoseTurnString = whoseTurnString,
                            errorMessage=errorMessage,
                            gameOverString=gameOverString,
                            gameOverBoolean=this_game["gameOver"],
                            getHTMLpath = '/getHTML/'+gameURL+'/'+player)


@app.route('/getHTML/<gameURL>/<player>')
def getHTML(gameURL, player):
    db = get_db()
    with db:
        cur = db.cursor()
        cur.execute("SELECT game_state FROM Game WHERE game_url = '%s'" % gameURL)
        this_game = json.loads(cur.fetchall()[0][0])

    grid = this_game["grid"]
    coin1 = str(this_game["coin1"])
    coin2 = str(this_game["coin2"])
    whoseTurn = this_game["upNext"]

    form = CoinForm()
    if whoseTurn == player:
        whoseTurnString = "your"
    else:
        whoseTurnString = "your partner's"

    whoseTurnHTML = "<strong>It's "+whoseTurnString+" turn!</strong><br><br>"

    if this_game["gameOver"]:
        whoseTurnHTML = "<strong><font color='lime'>GAME OVER! PLAYER "+this_game["winner"]+" WINS!</font></strong><br><br>"


    tableHTMLstring = "<table>"
    for y in range(6):
        tableHTMLstring = tableHTMLstring+"<tr>"
        for x in range(6):
            if grid[y][x][1] == "":
                tableHTMLstring = tableHTMLstring+"<td>"+str(grid[y][x][0])+"</td>"
            else:
                tableHTMLstring = tableHTMLstring+"<td>"+str(grid[y][x][1])+"</td>"

        tableHTMLstring = tableHTMLstring+"</tr>"

    tableHTMLstring = tableHTMLstring+"</table>"

    coinPositionHTMLstring = '<br><br><strong>The current\
            positions are: '+coin1+' and '+coin2+'</strong>'

    allHTML = whoseTurnHTML+tableHTMLstring+coinPositionHTMLstring
    return allHTML


# this is what makes our app start up when we run python views.py
# I'm pretty sure that the debug=True option makes it so that we don't need to
# restart the server each time we make a change to one of these files
if __name__ == '__main__':
    app.run(debug=True)
