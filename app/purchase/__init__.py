# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

asset = Blueprint('asset', __name__)

from . import views