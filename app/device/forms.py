# -*- coding: utf-8 -*-
#app/device/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

from ..models import Device, DeviceCategory
from ..forms import NonValidatingSelectFields
from ..documents import get_doc_list


class EditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.risk_analysis.choices = list(zip([''] + get_doc_list('risk_analysis'), [''] + get_doc_list('risk_analysis')))
        self.photo.choices = list(zip([''] + get_doc_list('photo'), [''] + get_doc_list('photo')))
        self.manual.choices = list(zip([''] + get_doc_list('manual'), [''] + get_doc_list('manual')))
        self.safety_information.choices = list(zip([''] + get_doc_list('safety_information'), [''] + get_doc_list('safety_information')))
        # self.category.choices = list(zip(Device.Category.get_list(), Device.Category.get_list()))
        self.category.choices = DeviceCategory.get_list_for_select()

    category = SelectField('Categorie', validators=[DataRequired()], coerce=int)
    brand = StringField('Merk', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    power = DecimalField('Vermogen', default=0.0)
    ce = BooleanField('CE')
    risk_analysis = NonValidatingSelectFields('Risicoanalyse')
    manual = NonValidatingSelectFields('Handleiding')
    safety_information = NonValidatingSelectFields('VIK')
    photo = NonValidatingSelectFields('Foto')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    """
    Add an asset
    """

class ViewForm(FlaskForm):
    category = StringField('Categorie', render_kw={'readonly':''})
    brand = StringField('Merk', render_kw={'readonly':''})
    type = StringField('Type', render_kw={'readonly':''})
    power = DecimalField('Vermogen', render_kw={'readonly':''})
    ce = BooleanField('CE', render_kw={'disabled':''})
    risk_analysis = StringField('Risicoanalyse', render_kw={'readonly':''})
    manual = StringField('Handleiding', render_kw={'readonly':''})
    safety_information = StringField('VIK', render_kw={'readonly':''})
    photo = StringField('Foto', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput(), render_kw={'readonly':''})
