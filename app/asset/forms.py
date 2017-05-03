# -*- coding: utf-8 -*-
#app/asset/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired

from ..models import Asset

class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_in_service = DateField('Date', validators=[DataRequired()])
    qr_code = StringField('QR', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    value = StringField('Value')
    location = StringField('Location')
    picture = StringField('Picture')
    description = TextAreaField('Description')


class AddForm(EditForm):
    """
    Add an asset
    """

