# forms.py

from flask_wtf import Form
from wtforms import TextField
from wtforms import DateField
from wtforms import TextAreaField
from wtforms import IntegerField
from wtforms import StringField
from wtforms.validators import DataRequired

class AssessmentForm(Form):
    title = TextField('title', validators=[DataRequired()])
    module_code = TextField('module_code', validators=[DataRequired()])
    deadline = DateField('deadline', format='%d-%m-%Y', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

class IdTypeForm(Form):
    id = IntegerField('id')
    type = StringField('type')
