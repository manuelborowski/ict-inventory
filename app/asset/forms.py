# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, DecimalField, FileField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
import datetime

from ..models import Asset, Supplier, Purchase, Device

def get_suppliers():
    return Supplier.query.all()


class UniqueQR:
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'An asset with this QR-code already exists'

    def __call__(self, form, field):
        asset_found = Asset.query.filter(Asset.qr_code == field.data).first()
        if 'id' in form:
            id =form.id.data
        else:
            id = None

        if asset_found and (id is None or id != asset_found.id):
            raise ValidationError(self.message)

class QRisValid():
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'A QR-code is a number or an URL ending with .../qr/123'

    def __call__(self, form, field):
        try:
            code = int(field.data)
        except:
            fl = field.data.split('/')
            lfl = len(fl)
            if lfl < 2 or fl[-2] != 'qr':
                raise ValidationError(self.message)
            try:
                code = int(fl[-1])
                field.data = fl[-1]
            except:
                raise ValidationError(self.message)


class EditForm(FlaskForm):
    name = StringField('Name')
    since = DateField('Date', validators=[DataRequired()], format='%d-%m-%Y', default=datetime.date.today)
    qr_code = StringField('QR', validators=[DataRequired(), QRisValid(), UniqueQR()], render_kw={'autofocus': 'true'})
    category = SelectField('Category', validators=[DataRequired()], choices=zip(Device.Category.get_list(), Device.Category.get_list()))
    status = SelectField('Status', validators=[DataRequired()], choices=zip(Asset.Status.get_list(), Asset.Status.get_list()))
    value = DecimalField('Value (&euro;)', default=0.0)
    supplier = QuerySelectField('Supplier', query_factory=get_suppliers)
    location = StringField('Location')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    """
    Add an asset
    """

class ViewForm(FlaskForm):
    name = StringField('Name', render_kw={'readonly':''})
    since = DateField('Date', render_kw={'readonly':''}, format='%d-%m-%Y')
    qr_code = StringField('QR', render_kw={'readonly':''})
    category = StringField('Category', render_kw={'readonly':''})
    status = StringField('Status', render_kw={'readonly':''})
    value = DecimalField('Value (&euro;)', render_kw={'readonly':''})
    supplier = StringField('Supplier', render_kw={'readonly':''})
    location = StringField('Location', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput())
