# -*- coding: utf-8 -*-
#app/device/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

from ..models import Device
from ..forms import NonValidatingSelectFields
from ..documents import get_doc_list


class EditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.risk_analysis.choices = zip([''] + get_doc_list('risk_analysis'), [''] + get_doc_list('risk_analysis'))
        self.photo.choices = zip([''] + get_doc_list('photo'), [''] + get_doc_list('photo'))
        self.manual.choices = zip([''] + get_doc_list('manual'), [''] + get_doc_list('manual'))
        self.safety_information.choices = zip([''] + get_doc_list('safety_information'), [''] + get_doc_list('safety_information'))
        self.category.choices = zip(Device.Category.get_list(), Device.Category.get_list())

    category = SelectField('Category', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    power = DecimalField('Power', default=0.0)
    ce = BooleanField('CE')
    risk_analysis = NonValidatingSelectFields('Risk Analyis')
    manual = NonValidatingSelectFields('Manual')
    safety_information = NonValidatingSelectFields('Safety Information')
    photo = NonValidatingSelectFields('Photo')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    """
    Add an asset
    """

class ViewForm(FlaskForm):
    category = StringField('Category', render_kw={'readonly':''})
    brand = StringField('Brand', render_kw={'readonly':''})
    type = StringField('Type', render_kw={'readonly':''})
    power = DecimalField('Power', render_kw={'readonly':''})
    ce = BooleanField('CE', render_kw={'readonly':''})
    risk_analysis = StringField('Risk Analyis', render_kw={'readonly':''})
    manual = StringField('Manual', render_kw={'readonly':''})
    safety_information = StringField('Safety Information', render_kw={'readonly':''})
    photo = StringField('Photo', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput(), render_kw={'readonly':''})
