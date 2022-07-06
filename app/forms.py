from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired

class DocumentUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])
    