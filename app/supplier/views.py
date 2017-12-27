# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required
from flask_table import Table, Col

from .forms import AddForm, EditForm, ViewForm
from .. import db
from . import supplier
from ..models import Supplier
from ..views import NoEscapeCol

class SupplierTable(Table):
    id = Col('Id')
    name = Col('Name')
    description = Col('Description')
    edit = NoEscapeCol('')
    view = NoEscapeCol('')
    delete = NoEscapeCol('')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'suppliertable', 'cellspacing': '0', 'width': '100%'}


#show a list of suppliers
@supplier.route('/supplier', methods=['GET', 'POST'])
@login_required
def suppliers():
    suppliers = Supplier.query.all()
    for s in suppliers:
        s.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(s.id) + "><i class='fa fa-trash'></i></a>")
        s.view = render_template_string("<a href=\"{{ url_for('supplier.view', id=" + str(s.id) + ") }}\"><i class='fa fa-eye'></i>")
        s.edit = render_template_string("<a href=\"{{ url_for('supplier.edit', id=" + str(s.id) + ") }}\"><i class='fa fa-pencil'></i>")
    suppliers_table = SupplierTable(suppliers)

    return render_template('supplier/suppliers.html', title='suppliers', route='supplier.supplier', subject='supplier', table=suppliers_table)


#add a new supplier
@supplier.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data,
                        description=form.description.data)
        db.session.add(supplier)
        db.session.commit()
        flash('You have added supplier {}'.format(supplier.name))

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
            flash('You have edited supplier {}'.format(supplier.name))

        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title='Edit')

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
    flash('You have successfully deleted the supplier.')

    return redirect(url_for('supplier.suppliers'))

