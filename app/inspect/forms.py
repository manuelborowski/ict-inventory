# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, IntegerField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
import datetime
from flask_login import current_user

from ..forms import NonValidatingSelectFields
from ..documents import get_doc_list

from ..models import Supplier, Device

def get_suppliers():
    return Supplier.query.order_by(Supplier.name).all()

def get_devices():
    return Device.query.order_by(Device.brand, Device.type).all()


class EditForm(FlaskForm):
    inspector = StringField('Controleur' )
    date = DateField('Datum', validators=[DataRequired()], format='%d-%m-%Y', default=datetime.date.today)
    info = StringField('Info')
    active = BooleanField('Actief', default=True)
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    inspector = StringField('Controleur', render_kw={'readonly':''})
    date = DateField('Datum', format='%d-%m-%Y', render_kw={'readonly':''})
    info = StringField('Info', render_kw={'readonly':''})
    active = BooleanField('Actief', render_kw={'disabled':''})
    id = IntegerField(widget=HiddenInput())
