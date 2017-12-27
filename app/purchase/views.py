# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from flask_table import Table, Col, DateCol, LinkCol

import datetime, time

#from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import purchase
from ..models import Purchase


#Special column to add html-tags.  Note : this can be dangerous, so whatch out!!!
class NoEscapeCol(Col):
    def td_format(self, content):
        return content

class PurchaseTable(Table):

    since = DateCol(_(u'Since'), date_format='dd-MM-YYYY')
    value = Col(_(u'Value'))      # value in euro
    delete = NoEscapeCol('')
    #edit = NoEscapeCol('')
    #view = NoEscapeCol('')
    id = Col('Id')
    copy_from = NoEscapeCol('C')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'purchasetable', 'cellspacing': '0', 'width': '100%'}


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

@purchase.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchases():
    purchases = Purchase.query.all()
    for p in purchases:
        p.copy_from = render_template_string("<input type='radio' name='copy_from' value='" + str(p.id) + "'>")
        p.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(p.id) + "><i class='fa fa-trash'></i></a>")
#        p.edit = render_template_string("<a href=\"{{ url_for('purchase.edit', id=" + str(p.id) + ") }}\"><i class='fa fa-pencil'></i>")
 #       p.view = render_template_string("<a href=\"{{ url_for('purchase.view', id=" + str(p.id) + ") }}\"><i class='fa fa-eye'></i>")
    purchase_table = PurchaseTable(purchases)

    return render_template('purchase/purchases.html', title='purchases', purchase_table=purchase_table, table_id='purchasetable', filter=filter)


#add a new purchase
@purchase.route('/purchase/add', methods=['GET', 'POST'])
@login_required
def add():
    pass
#     #qr_code can be inserted in 2 forms :
#     #regular number, e.g. 433
#     #complete url, e.g. http://blabla.com/qr/433.  If it contains http.*qr/, extract the number after last slash.
#     if 'copy_from' in request.form:
#         asset = Asset.query.get_or_404(int(request.form['copy_from']))
#         form = AddForm(obj=asset)
#         form.qr_code.data=''
#         #No idea why only these 2 fields need to be copied explicitly???
#         form.name.data = asset.name
#         form.location.data = asset.location
#     else:
#         form = AddForm()
#     del form.id # is not required here and makes validate_on_submit fail...
#     if not 'add' in request.form and form.validate_on_submit():
#         asset = Asset(name=form.name.data,
#                         date_in_service=form.date_in_service.data,
#                         qr_code=form.qr_code.data,
#                         category=form.category.data,
#                         status=form.status.data,
#                         value=form.value.data,
#                         location=form.location.data,
#                         picture=form.picture.data,
#                         supplier = form.supplier.data,
#                         db_status=Asset.DB_status.E_ACTIVE,
#                         description=form.description.data)
#         db.session.add(asset)
#         db.session.commit()
#         flash(_(u'You have added asset {}').format(asset.name))
#
#         return redirect(url_for('asset.assets'))
#
#    return render_template('purchase/purchase.html', form=form, title=_(u'Add'))
#
#
# #edit a asset
# @asset.route('/asset/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit(id):
#     asset = Asset.query.get_or_404(id)
#     form = EditForm(obj=asset)
#     if form.validate_on_submit():
#         if request.form['button'] == _(u'Save'):
#             form.populate_obj(asset)
#             db.session.commit()
#             flash(_(u'You have edited asset {}').format(asset.name))
#
#         return redirect(url_for('asset.assets'))
#
#     return render_template('asset/asset.html', form=form, title=_(u'Edit'))
#
# #no login required
# @asset.route('/asset/view/<int:id>', methods=['GET', 'POST'])
# def view(id):
#     asset = Asset.query.get_or_404(id)
#     form = ViewForm(obj=asset)
#     if form.validate_on_submit():
#         return redirect(url_for('asset.assets'))
#
#     return render_template('asset/asset.html', form=form, title=_(u'View'))
#
#
# #no login required
# @asset.route('/asset/qr/<string:qr>', methods=['GET', 'POST'])
# def view_via_qr(qr):
#     asset = Asset.query.filter_by(qr_code=qr).first_or_404()
#     form = ViewForm(obj=asset)
#     return render_template('asset/asset.html', form=form, title=_(u'View'))
#
# #delete an asset
# @asset.route('/asset/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete(id):
#     asset = Asset.query.get_or_404(id)
#     db.session.delete(asset)
#     db.session.commit()
#     flash(_('You have successfully deleted the asset.'))
#
#     return redirect(url_for('asset.assets'))
#
