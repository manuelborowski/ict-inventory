# -*- coding: utf-8 -*-
# app/settings/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user
from ..base import get_setting_inc_index_asset_name, set_setting_inc_index_asset_name
from . import settings
from .. import db, app
from ..models import Settings

import zipfile

def check_admin():
    if not current_user.is_admin:
        abort(403)

def get_settings_and_show():
    #inc_index_asset_name : if true and this asset is used as base to copy from, then the index of the asset name
    #will be incremented by one
    inc_index_asset_name = get_setting_inc_index_asset_name()
    print('>>> SETTINGS : {}'.format(inc_index_asset_name))
    return render_template('settings/settings.html', inc_index_asset_name=inc_index_asset_name)

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def show():
    return get_settings_and_show()

@settings.route('/settings/save', methods=['GET', 'POST'])
@login_required
def save():
    if request.form['button'] == 'Bewaar':
        print('Op de bewaar knop gedrukt')
        print(request.form)
        print(request.query_string)
        if 'inc_index_asset_name' in request.form:
            set_setting_inc_index_asset_name(True)
        else:
            set_setting_inc_index_asset_name(False)

    return get_settings_and_show()
