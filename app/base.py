# -*- coding: utf-8 -*-
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString
from wtforms import BooleanField
from flask import render_template, render_template_string, flash, redirect, url_for, request
import time

from models import Purchase, Device, Supplier
from .forms import CategoryFilter, DeviceFilter, StatusFilter, SupplierFilter




class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return HTMLString('<input %s>' % self.html_params(name=field.name, **kwargs))


class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


######################################################################################################
###                                       Build a generic filter
######################################################################################################

def check_date_in_form(date_key, form):
    if date_key in form and form[date_key] != '':
        try:
            time.strptime(form[date_key], '%d-%M-%Y')
            return form[date_key]
        except:
            flash(_(u'Wrong date format, must be of form d-m-y'))
    return None

def check_value_in_form(value_key, form):
    if value_key in form and form[value_key] != '':
        try:
            float(form[value_key])
            return form[value_key]
        except:
            flash(_(u'Wrong value format'))
    return None

def check_string_in_form(value_key, form):
    if value_key in form and form[value_key] != '':
        try:
            str(form[value_key])
            return form[value_key]
        except:
            flash(_(u'Wrong string format'))
    return None

def build_filter(table, since=False, value=False, location=False, category=False, status=False, supplier=False, device=False):
    filter = dict()
    il = table.query
    if (since or value) and table is not Purchase:
        il = il.join(Purchase)
    if (category or device) and table is not Device:
        il = il.join(Device)
    if supplier and table is not Supplier :
        il = il.join(Supplier)

    print '>>>>>>>>>>>>>>>>> ' + str(request.form   )

    if since:
        filter['since'] = 'True'
        date = check_date_in_form('date_after', request.form)
        if date:
            il = il.filter(Purchase.since > Purchase.reverse_date(date))
            filter['date_after'] = date
        date = check_date_in_form('date_before', request.form)
        if date:
            il = il.filter(Purchase.since < Purchase.reverse_date(date))
            filter['date_before'] = date
    if value:
        filter['value'] = 'True'
        value = check_value_in_form('value_from', request.form)
        if value:
            il = il.filter(Purchase.value > value)
            filter['value_from'] = value
        value = check_value_in_form('value_till', request.form)
        if value:
            il = il.filter(Purchase.value < value)
            filter['value_till'] = value
    if location:
        filter['location'] = 'True'
        value = check_string_in_form('room', request.form)
        if value:
            il = il.filter(table.location.contains(value))
            filter['room'] = value
    if category:
        filter['category'] = CategoryFilter()
        value = check_string_in_form('category', request.form)
        if value:
            il = il.filter(Device.category == value)
            filter['category'].category.data = value
    if status:
        filter['status'] = StatusFilter()
        value = check_string_in_form('status', request.form)
        if value:
            il = il.filter(table.status == value)
            filter['status'].status.data = value
    if supplier:
        filter['supplier'] = SupplierFilter()
        value = check_string_in_form('supplier', request.form)
        if value:
            il = il.filter(Supplier.name == value)
            filter['supplier'].supplier.data = value
    if device:
        filter['device'] = DeviceFilter()
        value = check_string_in_form('device', request.form)
        if value:
            s = value.split('/')
            il = il.filter(Device.brand==s[0].strip(), Device.type==s[1].strip())
            filter['device'].device.data = value
    il = il.all()
    return il, filter
