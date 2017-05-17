# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, DecimalField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
import datetime

from ..models import Asset, Supplier

def get_suppliers():
    return Supplier.query.all()

class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_in_service = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today)
    qr_code = StringField('QR', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=zip(Asset.Category.get_list(), Asset.Category.get_list()))
    status = SelectField('Status', validators=[DataRequired()], choices=zip(Asset.Status.get_list(), Asset.Status.get_list()))
    value = DecimalField('Value (&euro;)', default=0.0)
    supplier = QuerySelectField('Supplier', query_factory=get_suppliers)
    location = StringField('Location')
    picture = FileField('Picture')
    description = TextAreaField('Description')


class AddForm(EditForm):
    """
    Add an asset
    """

class ViewForm(FlaskForm):
    name = StringField('Name', render_kw={'readonly':''})
    date_in_service = DateField('Date', render_kw={'readonly':''})
    qr_code = StringField('QR', render_kw={'readonly':''})
    category = StringField('Category', render_kw={'readonly':''})
    status = StringField('Status', render_kw={'readonly':''})
    value = DecimalField('Value (&euro;)', render_kw={'readonly':''})
    supplier = StringField('Supplier', render_kw={'readonly':''})
    location = StringField('Location', render_kw={'readonly':''})
    picture = StringField('Picture', render_kw={'readonly':''})
    description = TextAreaField('Description', render_kw={'readonly':''})
