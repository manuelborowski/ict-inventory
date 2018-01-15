# -*- coding: utf-8 -*-
#app/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField
from models import Supplier, Device, Asset


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

class NonValidatingSelectFields(SelectField):
    def pre_validate(self, form):
        pass