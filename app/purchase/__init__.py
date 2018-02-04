# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

from flask_uploads import UploadSet, configure_uploads, ALL
import os

#the name of the uploadset is reused in UPLOADED_..._DEST
cms_path = 'commissioning'
cms_docs = UploadSet(cms_path, ALL)
cms_full_path = ''

def init_documents(app):
    global cms_full_path
    cms_full_path = os.path.join(app.config['STATIC_PATH'], cms_path)
    app.config['UPLOADED_COMMISSIONING_DEST'] = cms_full_path
    configure_uploads(app, cms_docs)


def get_cms_docs():
    cms_file_list = [""] + sorted(os.listdir(cms_full_path))
    return cms_file_list if cms_file_list else []

purchase = Blueprint('purchase', __name__)

from . import views
