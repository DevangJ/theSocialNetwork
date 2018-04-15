from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from flask_admin.form import widgets
from wtforms.fields.html5 import DateField

from db import *


def name_exists(form, field):
    if (field.data in username_fetch()):
        raise ValidationError('User with that username already exists.')

def name_not_mine_exists(form, field):
    if (field.data in username_not_mine_fetch()):
        raise ValidationError('User with that username already exists.')


def email_exists(form, field):
    if (field.data in email_fetch()):
        raise ValidationError('User with that email already exists.')

def email_not_mine_exists(form, field):
    if (field.data in email_not_mine_fetch()):
        raise ValidationError('User with that email already exists.')

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    dob  = DateField(
        'Your Birthday',
        format='%d/%m/%y',
        validators=[DataRequired()],
        widget=widgets.DatePickerWidget()
    )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(FlaskForm):
    content = TextAreaField("What's Up?", validators=[DataRequired()])


class ProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            )
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ])
    dob  = DateField(
        'Your Birthday',
        format='%d/%m/%y',
        validators=[DataRequired()],
        widget=widgets.DatePickerWidget()
    )
    bio = TextAreaField('Bio', validators=[DataRequired()])


class PasswordForm(FlaskForm):

    currentpassword = PasswordField(
        'Current Password',
        validators=[DataRequired()]
    )
    newpassword = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('newpassword2', message='Passwords must match')
        ])
    newpassword2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
