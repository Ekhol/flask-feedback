from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    """Form for user registration"""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=7, max=30)])
    email = StringField("Email", validators=[
                        InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging into the website"""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=7, max=30)])


class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(), Length(max=50)])
    content = StringField("Content", validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """empty"""
