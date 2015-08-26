from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/kitties')
def index():
    gamer = {"letter":"O"}
    return render_template('index.html',
                            title='Connect Factour!',
                            player = gamer)








