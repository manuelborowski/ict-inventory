# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import os

#the name of the uploadset is reused in UPLOADED_..._DEST
ra_path = 'riskanalysis'
ra_docs = UploadSet(ra_path, DOCUMENTS)
ra_full_path = ''

def init_documents(app):
    global ra_full_path
    ra_full_path = os.path.join(app.config['STATIC_PATH'], ra_path)
    app.config['UPLOADED_RISKANALYSIS_DEST'] = ra_full_path
    configure_uploads(app, ra_docs)


def get_ra_docs():
    ra_file_list = [""] + sorted(os.listdir(ra_full_path))
    return ra_file_list if ra_file_list else []


from flask import Blueprint

device = Blueprint('device', __name__)

from . import views