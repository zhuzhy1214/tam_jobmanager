from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


dict_func_description = {
    'func1': 'this is first function description',
    'func2': 'this is second function description',
    'pm-validation': 'this is a post mile validation function'
}
func_name = ['func1', 'func2', 'pm-validation']
class NewJobForm(FlaskForm):

    func_name = SelectField(label='Select function', choices=func_name)
    notes = TextAreaField('Content', validators=[DataRequired()])
    input_file = FileField('Upload input file', validators=[FileAllowed(['csv', 'xlsx'])])
    submit = SubmitField('Submit Job')

