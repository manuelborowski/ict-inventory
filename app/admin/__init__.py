# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views