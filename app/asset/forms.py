# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField,  IntegerField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
from .. import _

from ..models import Asset, Supplier, Purchase

def get_suppliers():
    return Supplier.query.all()

def get_purchases():
    return Purchase.query.all()


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
    location = StringField('Location')
    qr_code = StringField('QR', validators=[QRisValid(), UniqueQR()], render_kw={'autofocus': 'true'})
    status = SelectField('Status', validators=[DataRequired()], choices=zip(Asset.Status.get_list(), Asset.Status.get_list()))
    purchase = QuerySelectField('Purchase', query_factory=get_purchases)
    serial = StringField('Serial')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    name = StringField('Name', render_kw={'readonly':''})
    location = StringField('Location', render_kw={'readonly':''})
    qr_code = StringField('QR', render_kw={'readonly':''})
    status = StringField('Status', render_kw={'readonly':''})
    purchase = StringField('Purchase', render_kw={'readonly':''})
    since = DateField('Date', render_kw={'readonly':''}, format='%d-%m-%Y')
    value = DecimalField('Value (&euro;)', render_kw={'readonly':''})
    supplier = StringField('Supplier', render_kw={'readonly':''})
    category = StringField('Category', render_kw={'readonly':''})
    serial = StringField('Serial', render_kw={'readonly':''})

    brand = StringField(_(u'Brand'), render_kw={'readonly':''})
    type = StringField(_(u'Type'), render_kw={'readonly':''})
    power = DecimalField(_(u'Power'), render_kw={'readonly':''})
    ce = BooleanField(_(u'CE'), render_kw={'readonly':''})
    risk_analysis = StringField('Risk Analyis', render_kw={'readonly':''})
    manual = StringField('Manual', render_kw={'readonly':''})
    safety_information = StringField('Safety Information', render_kw={'readonly':''})
    photo = StringField('Photo', render_kw={'readonly':''})


    id = IntegerField(widget=HiddenInput())
