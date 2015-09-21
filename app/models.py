from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameURL = db.Column(db.String(64), index=True, unique=True)
    gameState = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Game %r>' % (self.gameURL)
