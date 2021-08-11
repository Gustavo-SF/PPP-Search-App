from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

TYPES = [(1,"Closest cluster"), (2, "Closest materials")]

class SearchForm(FlaskForm):
    q = StringField('Name to search', validators=[DataRequired()])
    type_of_search = SelectField("Type of search", choices=TYPES, validators=[DataRequired()])
    submit = SubmitField('Search')