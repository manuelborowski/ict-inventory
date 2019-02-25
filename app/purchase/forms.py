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

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.commissioning.choices = zip([''] + get_doc_list('commissioning'), [''] + get_doc_list('commissioning'))

    since = DateField('Datum', validators=[DataRequired()], format='%d-%m-%Y', default=datetime.date.today)
    value = DecimalField('Bedrag (&euro;)', default=0.0)
    supplier = QuerySelectField('Leverancier', query_factory=get_suppliers)
    device = QuerySelectField('Toestel', query_factory=get_devices)
    commissioning = NonValidatingSelectFields('Indienststelling')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    """
    Add a purchase
    """

class ViewForm(FlaskForm):
    since = DateField('Datum', render_kw={'readonly':''}, format='%d-%m-%Y')
    value = DecimalField('Bedrag (&euro;)', render_kw={'readonly':''})
    supplier = StringField('Leverancier', render_kw={'readonly':''})
    device = StringField('Toestel', render_kw={'readonly':''})
    commissioning = StringField('Indienststelling', render_kw={'readonly':''})


    picture = StringField('Foto', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput())
