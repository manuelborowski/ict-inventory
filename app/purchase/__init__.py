# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import os

#the name of the uploadset is reused in UPLOADED_..._DEST
cms_docs = UploadSet('commissioning', DOCUMENTS)
cms_docs_path = 'app/static/commissioning'

def init_documents(app):
    app.config['UPLOADED_COMMISSIONING_DEST'] = cms_docs_path
    configure_uploads(app, cms_docs)


def get_cms_docs():
    cms_file_list = sorted(os.listdir(cms_docs_path))
    cms_file_list = [""] + cms_file_list
    return cms_file_list if cms_file_list else []

purchase = Blueprint('purchase', __name__)

from . import views
