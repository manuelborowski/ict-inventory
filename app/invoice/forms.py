# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
import datetime

from ..forms import NonValidatingSelectFields
from ..documents import get_doc_list

from ..models import Supplier, Device

def get_suppliers():
    return Supplier.query.order_by(Supplier.name).all()

def get_devices():
    return Device.query.order_by(Device.brand, Device.type).all()


class EditForm(FlaskForm):
    number = StringField('Factuur')
    since = DateField('Datum', validators=[DataRequired()], format='%d-%m-%Y', default=datetime.date.today)
    supplier = QuerySelectField('Leverancier', query_factory=get_suppliers)
    info = StringField('Info')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    number = StringField('Factuur', render_kw={'readonly':''})
    since = DateField('Datum', render_kw={'readonly':''}, format='%d-%m-%Y')
    supplier = StringField('Leverancier', render_kw={'readonly':''})
    info = StringField('Info', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput())
