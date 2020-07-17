from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

class PhotoForm(FlaskForm):
    """flask_wtf form class the file upload"""
    photo = FileField('image', validators=[
        FileRequired()
    ])