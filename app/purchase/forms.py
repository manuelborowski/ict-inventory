# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, DecimalField, FileField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
import datetime, os

from ..forms import NonValidatingSelectFields
from ..upload import get_commissioning_docs

from ..models import Purchase, Supplier, Device

def get_suppliers():
    return Supplier.query.all()

def get_devices():
    return Device.query.all()


class EditForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.commissioning.choices = zip(get_commissioning_docs(), get_commissioning_docs())

    since = DateField('Date', validators=[DataRequired()], format='%d-%m-%Y', default=datetime.date.today)
    value = DecimalField('Value (&euro;)', default=0.0)
    supplier = QuerySelectField('Supplier', query_factory=get_suppliers)
    device = QuerySelectField('Device', query_factory=get_devices)
    commissioning = NonValidatingSelectFields('Commissioning')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    """
    Add a purchase
    """

class ViewForm(FlaskForm):
    since = DateField('Date', render_kw={'readonly':''}, format='%d-%m-%Y')
    value = DecimalField('Value (&euro;)', render_kw={'readonly':''})
    supplier = StringField('Supplier', render_kw={'readonly':''})
    device = StringField('Device', render_kw={'readonly':''})
    commissioning = StringField('Commissioning', render_kw={'readonly':''})


    picture = StringField('Picture', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput())
