# -*- coding: utf-8 -*-
#app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import HiddenInput

from app.models import User


class EditForm(FlaskForm):
    name = StringField('Naam', render_kw={'readonly':''})
    active = BooleanField('Actief')
    info = StringField('Info')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    name = StringField('Naam', validators=[DataRequired()])
    pass


class ViewForm(FlaskForm):
    name = StringField('Naam', render_kw={'readonly':''})
    active = BooleanField('Actief', render_kw={'disabled':''})
    info = StringField('Info', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput())
