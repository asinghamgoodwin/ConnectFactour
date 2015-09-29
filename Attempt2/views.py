"""this will render html templates depending on what url we go to"""
from flask import Flask, render_template, g
import sqlite3
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional
from models import *
from connectFactour import *
from contextlib import closing

app = Flask(__name__)
# this is referencing our config.py file, and weirdly lets us get away with not using a secret key
app.config.from_object("config")

class CoinForm(Form):
    # doing validators=[DataRequired()] did not work for the SelectField
    coin1 = RadioField('category',
                       choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                       validators=[Optional()])

    coin2 = RadioField('category',
                       choices=[("1","1"),("2","2"),("3","3"),("4","4"),
                                ("5","5"),("6","6"),("7","7"),("8","8"),("9","9")], 
                       validators=[Optional()])

# @app.route('/')
# @app.route('/index')
# @app.route('/kitties')
@app.route('/index', methods = ["GET", "POST"])
def index():
    gamer1 = gamer('X')
    gamer2 = gamer('O')
    newGame = game(gamer1, gamer2)
    coinForm = CoinForm()
    if coinForm.validate_on_submit():
        print coinForm.coin1.data
        print coinForm.coin2.data
    return render_template('index.html',
                            title='Connect Factour!',
                            form=coinForm,
                            game=newGame)




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
