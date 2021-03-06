# -*- coding: utf-8 -*-
#app/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField
from .models import Supplier, Device, Asset, DeviceCategory


class CategoryFilter(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(CategoryFilter, self).__init__(*args, **kwargs)
        self.category.choices=DeviceCategory.get_list_for_select_first_empty()

    category = SelectField('')

class StatusFilter(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(StatusFilter, self).__init__(*args, **kwargs)
        self.status.choices=list(zip(Asset.Status.get_list_with_empty(), Asset.Status.get_list_with_empty()))

    status = SelectField('')

class SupplierFilter(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(SupplierFilter, self).__init__(*args, **kwargs)
        sl = Supplier.query.order_by(Supplier.name).all()
        sl.insert(0, '')
        self.supplier.choices=list(zip(sl, sl))

    supplier = SelectField('')

class DeviceFilter(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(DeviceFilter, self).__init__(*args, **kwargs)
        dl = Device.query.order_by(Device.brand).all()
        dl.insert(0, '')
        self.device.choices=list(zip(dl, dl))

    device = SelectField('')

class NonValidatingSelectFields(SelectField):
    def pre_validate(self, form):
        pass