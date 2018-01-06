# -*- coding: utf-8 -*-
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString
from wtforms import BooleanField
from flask import render_template, render_template_string, flash, redirect, url_for, request, get_flashed_messages
import time

from models import Asset, Purchase, Device, Supplier
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
            time.strptime(form[date_key].strip(), '%d-%M-%Y')
            return form[date_key].strip()
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

def build_filter(table, template, since=False, value=False, location=False, category=False, status=False, supplier=False, device=False):
    __filter = {}
    #depending on the table, multiple joins are required to get the necessary data
    il = table.query
    if (since or value) and table is not Purchase:
        il = il.join(Purchase)
    if (category or device) and table is not Device:
        il = il.join(Device)
    if supplier and table is not Supplier :
        il = il.join(Supplier)

    __total_count = il.count()

    #Create the sql-request with the appriorate filters
    if since:
        __filter['since'] = 'True'
        date = check_date_in_form('date_after', request.values)
        if date:
            il = il.filter(Purchase.since >= Purchase.reverse_date(date))
            __filter['date_after'] = date
        date = check_date_in_form('date_before', request.values)
        if date:
            il = il.filter(Purchase.since <= Purchase.reverse_date(date))
            __filter['date_before'] = date
    if value:
        __filter['value'] = 'True'
        value = check_value_in_form('value_from', request.values)
        if value:
            il = il.filter(Purchase.value >= value)
            __filter['value_from'] = value
        value = check_value_in_form('value_till', request.values)
        if value:
            il = il.filter(Purchase.value <= value)
            __filter['value_till'] = value
    if location:
        __filter['location'] = 'True'
        value = check_string_in_form('room', request.values)
        if value:
            il = il.filter(table.location.contains(value))
            __filter['room'] = value
    if category:
        __filter['category'] = CategoryFilter()
        value = check_string_in_form('category', request.values)
        if value:
            il = il.filter(Device.category == value)
            __filter['category'].category.data = value
    if status:
        __filter['status'] = StatusFilter()
        value = check_string_in_form('status', request.values)
        if value:
            il = il.filter(table.status == value)
            __filter['status'].status.data = value
    if supplier:
        __filter['supplier'] = SupplierFilter()
        value = check_string_in_form('supplier', request.values)
        if value:
            il = il.filter(Supplier.name == value)
            __filter['supplier'].supplier.data = value
    if device:
        __filter['device'] = DeviceFilter()
        value = check_string_in_form('device', request.values)
        if value:
            s = value.split('/')
            il = il.filter(Device.brand==s[0].strip(), Device.type==s[1].strip())
            __filter['device'].device.data = value

    __filtered_count = il.count()

    #order, if required
    column_number = check_value_in_form('order[0][column]', request.values)
    if column_number:
        column_name = check_string_in_form('columns[' + str(column_number) + '][data]', request.values)
        direction = check_string_in_form('order[0][dir]', request.values)
        if direction == 'desc':
            il = il.order_by(template[int(column_number)]['order_by'].desc())
        else:
            il = il.order_by(template[int(column_number)]['order_by'])

        #paginate, if required
        start = int(check_value_in_form('start', request.values))
        length = int(check_value_in_form('length', request.values))
        il = il.slice(start, start+length)

    il = il.all()

    print '>>>>>>>>> total/filtered {}/{}'.format(__total_count, __filtered_count)

    return il, __total_count, __filtered_count, __filter




asset_template = [{'name': 'Name', 'data':'name', 'order_by': Asset.name},
      {'name': 'Category', 'data':'purchase.device.category', 'order_by': Device.category},
      {'name': 'Location', 'data':'location', 'order_by': Asset.location},
      {'name': 'Since', 'data':'purchase.since', 'order_by': Purchase.since},
      {'name': 'Value', 'data':'purchase.value', 'order_by': Purchase.value},
      {'name': 'QR', 'data':'qr_code', 'order_by': Asset.qr_code},
      {'name': 'Status', 'data':'status', 'order_by': Asset.status},
      {'name': 'Supplier', 'data':'purchase.supplier.name', 'order_by': Supplier.name},
      {'name': 'Device', 'data':'purchase.device.brandtype', 'order_by': Device.brand},
      {'name': 'Serial', 'data': 'serial', 'order_by': Asset.serial},
      ]
