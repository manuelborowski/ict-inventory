# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required
from flask_table import Table, Col

from .forms import AddForm, EditForm, ViewForm, CategoryFilter, DeviceFilter, StatusFilter, SupplierFilter
from .. import db
from . import supplier
from ..models import Supplier, Asset, Purchase, Device
from ..views import NoEscapeCol

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration

#    class SupplierTable(Table):
#     id = Col('Id')
#     name = Col('Name')
#     description = Col('Description')
#     edit = NoEscapeCol('')
#     view = NoEscapeCol('')
#     delete = NoEscapeCol('')
#     classes = ['table ' 'table-striped ' 'table-bordered ']
#     html_attrs = {'id': 'suppliertable', 'cellspacing': '0', 'width': '100%'}
#
#
#
# #show a list of suppliers
# @supplier.route('/supplier', methods=['GET', 'POST'])
# @login_required
# def suppliers():
#     suppliers, filter = build_filter(Supplier, supplier=True)
#
#     for s in suppliers:
#         s.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(s.id) + "><i class='fa fa-trash'></i></a>")
#         s.view = render_template_string("<a href=\"{{ url_for('supplier.view', id=" + str(s.id) + ") }}\"><i class='fa fa-eye'></i>")
#         s.edit = render_template_string("<a href=\"{{ url_for('supplier.edit', id=" + str(s.id) + ") }}\"><i class='fa fa-pencil'></i>")
#     suppliers_table = SupplierTable(suppliers)
#
#     return render_template('base_multiple_items.html', title='suppliers', route='supplier.suppliers', subject='supplier', table=suppliers_table, filter=filter)
#


#This route is called by an ajax call on the assets-page to populate the table.
@supplier.route('/supplier/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['supplier'])

#ashow a list of suppliers
@supplier.route('/supplier', methods=['GET', 'POST'])
@login_required
def suppliers():
    #The following line is required only to build the filter-fields on the page.
    __filter, __filter_form, a,b, c = build_filter(tables_configuration['supplier'])
    return render_template('base_multiple_items.html', title='suppliers', route='supplier.suppliers', subject='supplier',
                           header_list=tables_configuration['supplier']['template'], filter=__filter, filter_form=__filter_form,
                           delete_message="Are you sure you want to delete this supplier AND all associated purchases AND assets?")


#add a new supplier
@supplier.route('/supplier/add/<int:id>', methods=['GET', 'POST'])
@supplier.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    if id > -1:
        supplier = Supplier.query.get_or_404(int(id))
        form = AddForm(obj=supplier)
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    if not 'add' in request.form and form.validate_on_submit():
        supplier = Supplier(name=form.name.data,
                        description=form.description.data)
        db.session.add(supplier)
        db.session.commit()
        #flash('You have added supplier {}'.format(supplier.name))

        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title='Add')


#edit a supplier
@supplier.route('/supplier/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    supplier = Supplier.query.get_or_404(id)
    form = EditForm(obj=supplier)
    if form.validate_on_submit():
        if request.form['button'] == 'Save':
            form.populate_obj(supplier)
            db.session.commit()
            #flash('You have edited supplier {}'.format(supplier.name))

        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title=_('Edit a supplier'), role='edit', subject='supplier', route='supplier.suppliers')

#no login required
@supplier.route('/supplier/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    supplier = Supplier.query.get_or_404(id)
    form = ViewForm(obj=supplier)
    if form.validate_on_submit():
        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title=_('View a supplier'), role='view', subject='supplier', route='supplier.suppliers')


#delete a supplier
@supplier.route('/supplier/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    #flash('You have successfully deleted the supplier.')

    return redirect(url_for('supplier.suppliers'))

