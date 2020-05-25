# -*- coding: utf-8 -*-
# app/settings/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user
from ..base import get_setting_inc_index_asset_name, set_setting_inc_index_asset_name, get_setting_copy_from_last_add, set_setting_copy_from_last_add
from . import settings
from .. import db, app, user_plus_required
from ..models import Settings
from flask_login import current_user

import zipfile

def check_admin():
    if not current_user.is_admin:
        abort(403)

def get_settings_and_show():
    #inc_index_asset_name : if true and this asset is used as base to copy from, then the index of the asset name
    #will be incremented by one
    inc_index_asset_name = get_setting_inc_index_asset_name()
    #copy_from_last_add : if a url-shortcut with qr code is uses, and the qr code is not found, then a new asset is
    #added which is a copy from the previous added asset.
    copy_from_last_add = get_setting_copy_from_last_add()
    return render_template('settings/settings.html',
                           inc_index_asset_name=inc_index_asset_name,
                           copy_from_last_add=copy_from_last_add)

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
@user_plus_required
def show():
    return get_settings_and_show()

@settings.route('/settings/save', methods=['GET', 'POST'])
@login_required
@user_plus_required
def save():
    if request.form['button'] == 'Bewaar':
        set_setting_inc_index_asset_name(True if 'inc_index_asset_name' in request.form else False)
        set_setting_copy_from_last_add(True if 'copy_from_last_add' in request.form else False)

    return get_settings_and_show()
