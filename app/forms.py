from tokenize import String
from wsgiref.validate import validator
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    submit  = SubmitField('submit')
    
class BookUpdateForm(FlaskForm):
    price = IntegerField('price', validators=[DataRequired()])
    photo = FileField('photo')
    submit = SubmitField('update')
    
class AuthorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class AuthorUpdateForm(FlaskForm):
    photo = FileField('photo')
    submit = SubmitField('update')