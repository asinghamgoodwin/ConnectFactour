"""this will render html templates depending on what url we go to"""
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

app = Flask(__name__)
# this is referencing our config.py file, and weirdly lets us get away with not using a secret key
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
                "gameOver": False
    }  
class CoinForm(Form):
    # doing validators=[DataRequired()] did not work for the SelectField
    coin1 = RadioField('category',
                    choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                    #validators=[EqualTo("5", message='must equal 5')])
                    validators=[Optional()])

    coin2 = RadioField('category',
                    choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                    validators=[Optional()])


@app.route('/newGame',methods = ["GET","POST"])
def newGame():
    gameURL =''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.digits) for _ in range(8)) 
    myURL = '/index/'+gameURL+'/X'
    partnerURL = '/index/'+gameURL+'/O'
    form = NewGameForm()
    #print gameURL
    if form.validate_on_submit():
#        print "I validated"
        newGame_state =  defaultGame
        newGame_state["coin1"] = random.randint(1,9)
        newGame_state["coin2"] = random.randint(1,9)
        
        # MAKE A NEW ENTRY INTO THE SQL DATABASE
        db = get_db()
        with db:
            cur = db.cursor()
            cur.execute("insert into Game(game_state,game_url) values (?,?)", [json.dumps(newGame_state),gameURL])
#        print myURL
        return redirect(myURL)
    return render_template('newGame.html',
                            partnerURL=partnerURL,
                            form=form)

@app.route('/index/<gameURL>/<player>', methods = ["GET", "POST"])
def index(gameURL, player):
#    print gameURL
#    print player
    db = get_db()
    with db:
        cur = db.cursor()
        cur.execute("SELECT game_state FROM Game WHERE game_url = '%s'" % gameURL)
        this_game = json.loads(cur.fetchall()[0][0])
     #   this_game_type = type(this_game)


    coin1 = str(this_game['coin1'])
    coin2 = str(this_game['coin2'])
    coinPositionHTMLstring = 'The current positions are: '+coin1+' and '+coin2

    #pretendGame = defaultGame
    if player == "X":
        otherPlayer = 'O'
    else:
        otherPlayer = 'X'
    #partnerURL = gameURL+"/"+otherPlayer

    coinForm = CoinForm()
    print "I'm about to do the if statement! I'm player "+player
    if coinForm.validate_on_submit():
        print "I validated on submit! Player: "+player
        #print type(coinForm.coin1.data)
        coin1 = int(coinForm.coin1.data)
        coin2 = int(coinForm.coin2.data)
        product = coin1*coin2
        for r, row in enumerate(this_game["grid"]):
            for c, cell in enumerate(row):
                if int(cell[0]) == product:
                    cell[1] = player
        this_game['coin1'] = coin1
        this_game['coin2'] = coin2
        this_game["upNext"] = otherPlayer

        # print this_game['upNext']
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
                            #partnerURL=partnerURL,
                            gameURL=gameURL,
                            otherPlayer=otherPlayer,
                            myLetter=player,
                            coinPositionHTMLstring=coinPositionHTMLstring,
                            whoseTurnString = whoseTurnString,
                            getHTMLpath = '/getHTML/'+gameURL+'/'+player)


@app.route('/getGameState/<gameURL>')
## def getGameState(gameURL):
##     db = get_db()
##     with db:
##         cur = db.cursor()
##         cur.execute("SELECT game_state FROM Game WHERE game_url = '%s'" % gameURL)
##         this_game = (cur.fetchall()[0][0])
##     return this_game


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

    tableHTMLstring = "<table>"
    for y in range(6):
        tableHTMLstring = tableHTMLstring+"<tr>"
        for x in range(6):
            if grid[y][x][1] == "":
                tableHTMLstring = tableHTMLstring+"<td>"+str(grid[y][x][0])+"</td>"
            else:
                tableHTMLstring = tableHTMLstring+"<td>"+str(grid[y][x][1])+"</td>"

        tableHTMLstring = tableHTMLstring+"</tr>"

          #<font color ="red"> <td>{{ grid[y][x][1] }} </td></font>
          #{% else %}
          #    <td>{{ grid[y][x][1] }} </td>

    tableHTMLstring = tableHTMLstring+"</table>"

    coinPositionHTMLstring = '<br><br><strong>The current positions are: '+coin1+' and '+coin2+'</strong>'
## 
##     formHTMLstring = '<form action="" method="post">'
## 
##     formHTMLstring = formHTMLstring+str(form.hidden_tag())+'<br>'
## 
##     for subfield in form.coin1:
##         formHTMLstring = formHTMLstring+'<tr>'+str(subfield)+str(subfield.label)+'</tr>'
##     formHTMLstring =formHTMLstring+' <br> <br>'
## 
##     for subfield in form.coin2:
##         formHTMLstring = formHTMLstring+'<tr>'+str(subfield)+str(subfield.label)+'</tr>'
##     formHTMLstring =formHTMLstring+' <br> <br> <input type = "submit" value = "Make move!"> </form>'
##     
    allHTML = whoseTurnHTML+tableHTMLstring+coinPositionHTMLstring
    return allHTML




    ## 
    ## # @app.route('/')
    ## # the GET is important to display the form and stuff, and the POST lets us grab the form input
    ## @app.route('/index', methods = ["GET", "POST"])
## def SALADindex():
##     # opening a connection to our database (get_db comes from models)
##     db = get_db()
##     # with db:
##     with closing(db.cursor()) as cur:
##         # cur = db.cursor()
##         form = SaladForm()
## 
##         ### this section is to get the categories from our category table to use as drop-down choices
##         cur.execute('SELECT category from category')
##         categoryList = cur.fetchall()
##         # the categories come as tuples, but we only want the first part, x[0]
##         # these come as unicode strings, and we can .encode('utf8') to make them pretty, normal strings
##         category_tuples = [(x[0].encode('utf8'),x[0].encode('utf8')) for x in categoryList]
##         form.add_category_choices(category_tuples)
##     # db.close()
## 
##     ### this section is for pretty printing
##     # db = get_db()
##     # with db:
##     # with closing(db.cursor()) as cur:
##         # cur = db.cursor()
## 
##         if form.validate_on_submit():
##             print "I validated on submit"
##             cur.execute('insert into Ingredient (person, category, ingredient) values (?, ?, ?)', 
##                         [form.name.data, form.category.data, form.ingredient.data])
##             # print categoryList
##             # print form.name.data
##             # print form.category.data
##         else:
##             print "I didn't validate"
##     # could we also use close_connection() ?
##         db.commit()
##         cur.execute('SELECT person, category, ingredient FROM Ingredient')            
##         IngredientTableTuples = cur.fetchall()
##         categories = [x[0] for x in category_tuples]
##         categories_for_printing = {}
##         for cat in categories:
##             categories_for_printing[cat] = [(x[2].encode('utf8'), x[0].encode('utf8')) for x in IngredientTableTuples if x[1] == cat]
##             
##         #print categories_for_printing
##     db.close()
## 
##     ourRatios = sm.calculateRatios(categories_for_printing)
##     warningsList = sm.warnAboutRatios(sm.perfectSaladRatios, ourRatios)
##     warningsString = ", ".join(warningsList)
##     print warningsString
##     # pretend_ingredients = ["cats", "spinace", "avodabo", "carobs"]
##     # pretend_categories = ["greebs", "vebebbggeez", "FROOBs"]
##     return render_template('index.html',
##             form=form,
##             categoryDict = categories_for_printing,
##             warnings = warningsString)
##             # ingredient_list=pretend_ingredients,
##             # categories=pretend_categories)
## 


# this is what makes our app start up when we run python views.py
# I'm pretty sure that the debug=True option makes it so that we don't need to
# restart the server each time we make a change to one of these files
if __name__ == '__main__':
    app.run(debug=True)
