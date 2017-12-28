# -*- coding: utf-8 -*-
#app/suppliers/forms.py

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
from ..models import Supplier, Device, Asset

class UniqueName:
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'A supplier with this name already exists'

    def __call__(self, form, field):
        supplier_found = Supplier.query.filter(Supplier.name == field.data).first()
        if 'id' in form:
            id =form.id.data
        else:
            id = None

        if supplier_found and (id is None or id != supplier_found.id):
            raise ValidationError(self.message)


class EditForm(FlaskForm):
    """
    Edit an existing supplier
    """

    name = StringField('Name', validators=[DataRequired(), UniqueName()])
    description = TextAreaField('Description')
    id = IntegerField(widget=HiddenInput())


class AddForm(EditForm):
    """
    Add a supplier
    """

class ViewForm(FlaskForm):
    """
    Edit an existing supplier
    """
    name = StringField(_(u'Name'), render_kw={'readonly':''})
    description = TextAreaField('Description', render_kw={'readonly':''})
    id = IntegerField(widget=HiddenInput(), render_kw={'readonly':''})

class CategoryFilter(FlaskForm):
    category = SelectField('', choices=zip(Device.Category.get_list_with_empty(), Device.Category.get_list_with_empty()))

class StatusFilter(FlaskForm):
    status = SelectField('', choices=zip(Asset.Status.get_list_with_empty(), Asset.Status.get_list_with_empty()))

class SupplierFilter(FlaskForm):
    sl = Supplier.query.all()
    sl.insert(0, '')
    supplier = SelectField('', choices=zip(sl, sl))

class DeviceFilter(FlaskForm):
    dl = Device.query.all()
    dl.insert(0, '')
    device = SelectField('', choices=zip(dl, dl))
