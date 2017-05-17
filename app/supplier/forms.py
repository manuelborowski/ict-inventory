# -*- coding: utf-8 -*-
#app/suppliers/forms.py

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import HiddenInput
from ..models import Supplier

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

