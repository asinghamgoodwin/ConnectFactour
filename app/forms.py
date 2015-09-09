from flask.ext.wtf import Form
from wtforms import RadioField
from wtforms.validators import DataRequired

class coinMoveForm(Form):
    coin1 = RadioField('coin1', choices=[('1','1'),('2','2'),('3','3'),
        ('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9')])
    coin2 = RadioField('coin2', choices=[('1','1'),('2','2'),('3','3'),
        ('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9')])
