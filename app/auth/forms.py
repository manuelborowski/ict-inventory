# -*- coding: utf-8 -*-
#app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User


class LoginForm(FlaskForm):
    """
    For users who want to log in
    """
    username = StringField('Username', validators=[DataRequired()], render_kw={'autofocus': 'true'})
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
