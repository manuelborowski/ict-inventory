# -*- coding: utf-8 -*-
#app/device/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput

from ..models import Device, DeviceCategory, ControlCardTemplate
from ..forms import NonValidatingSelectFields
from ..documents import get_doc_list


class EditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.risk_analysis.choices = list(zip([''] + get_doc_list('risk_analysis'), [''] + get_doc_list('risk_analysis')))
        self.photo.choices = list(zip([''] + get_doc_list('photo'), [''] + get_doc_list('photo')))
        self.manual.choices = list(zip([''] + get_doc_list('manual'), [''] + get_doc_list('manual')))
        self.safety_information.choices = list(zip([''] + get_doc_list('safety_information'), [''] + get_doc_list('safety_information')))
        self.category_id.choices = DeviceCategory.get_list_for_select()

    category_id = SelectField('Categorie', validators=[DataRequired()], coerce=int)
    brand = StringField('Merk', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    power = DecimalField('Vermogen', default=0.0)
    ce = BooleanField('CE')
    control_template = QuerySelectField('Inspectie Fiche', query_factory=ControlCardTemplate.get_all, default=ControlCardTemplate.get_default)
    risk_analysis = NonValidatingSelectFields('Risicoanalyse')
    manual = NonValidatingSelectFields('Handleiding')
    safety_information = NonValidatingSelectFields('VIK')
    photo = NonValidatingSelectFields('Foto')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        self.category_id.choices = DeviceCategory.get_list_for_select()

    category_id = SelectField('Categorie', render_kw={'readonly':''})
    brand = StringField('Merk', render_kw={'readonly':''})
    type = StringField('Type', render_kw={'readonly':''})
    power = DecimalField('Vermogen', render_kw={'readonly':''})
    ce = BooleanField('CE', render_kw={'disabled':''})
    control_template = StringField('Inspectie Fiche', render_kw={'readonly':''})
    risk_analysis = StringField('Risicoanalyse', render_kw={'readonly':''})
    manual = StringField('Handleiding', render_kw={'readonly':''})
    safety_information = StringField('VIK', render_kw={'readonly':''})
    photo = StringField('Foto', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput(), render_kw={'readonly':''})
