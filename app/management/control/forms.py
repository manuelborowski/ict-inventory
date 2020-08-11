# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField,  IntegerField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
#from .. import _

from ...models import ControlCardTemplate


class EditForm(FlaskForm):
    name = StringField('Naam')
    info = StringField('Info')
    active = BooleanField('Actief')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    name = StringField('Naam', render_kw={'readonly':''})
    info = StringField('Info', render_kw={'readonly':''})
    active = BooleanField('Actief', render_kw={'disabled':''})
    id = IntegerField(widget=HiddenInput())
