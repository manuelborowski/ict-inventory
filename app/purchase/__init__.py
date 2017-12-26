# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

purchase = Blueprint('purchase', __name__)

from . import views