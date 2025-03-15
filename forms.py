from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields import DateField
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'login'

class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = StringField('Price')
    appropriate = StringField('Appropriate')
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Book')

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Author')

class EditbookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = StringField('Price')
    appropriate = StringField('Appropriate')
    author = SelectField('Author', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditauthorForm(FlaskForm):
    author_select = SelectField(
        'Select Author', 
        coerce=int,
        validators=[DataRequired()],
        choices=[]
    )
    new_name = StringField(
        'New Name', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')