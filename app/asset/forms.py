# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from ..models import Asset


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_in_service = DateField('Date', validators=[DataRequired()])
    qr_code = StringField('QR', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=zip(Asset.Category.get_list(), Asset.Category.get_list()))
    status = SelectField('Status', validators=[DataRequired()], choices=zip(Asset.Status.get_list(), Asset.Status.get_list()))
    value = StringField('Value')
    location = StringField('Location')
    picture = StringField('Picture')
    description = TextAreaField('Description')


class AddForm(EditForm):
    """
    Add an asset
    """

