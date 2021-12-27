from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask import current_app

# available functions
func_list = [
    'Inventory data check',
    'Pavement condition assessment',
    'Post mile validation',
    'Add columns'
]

class NewJobForm(FlaskForm):

    func_name = SelectField(label='Select function', choices=func_list)
    notes = TextAreaField('Content', validators=[DataRequired()])
    input_file = FileField('Upload input file',
                           validators=[FileAllowed(['csv', 'xlsx'])]
                           )
    submit = SubmitField('Submit Job')
