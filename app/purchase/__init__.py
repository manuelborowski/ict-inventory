# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

from flask_uploads import UploadSet, configure_uploads, DOCUMENTS


#the name of the uploadset is reused in UPLOADED_..._DEST
cms_docs = UploadSet('commissioning', DOCUMENTS)
cms_docs_path = 'static/commissioning'

def init_documents(app):
    app.config['UPLOADED_COMMISSIONING_DEST'] = cms_docs_path
    configure_uploads(app, cms_docs)

purchase = Blueprint('purchase', __name__)

from . import views
