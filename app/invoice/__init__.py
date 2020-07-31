# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

invoice = Blueprint('invoice', __name__)

from . import views
