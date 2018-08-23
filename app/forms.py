from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    relationship = StringField('Predicate', validators=[DataRequired()])
    object = StringField('Object', validators=[DataRequired()])
    submit = SubmitField('Search')
