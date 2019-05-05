from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

'''

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

'''

from wtforms import Form, StringField

class SearchForm(Form):
    #choices = [('Movies', 'Movies'),
    #           ('Users', 'Users')]
    #select = SelectField('', choices=choices)
    search = StringField('', render_kw={'maxlength': 15})