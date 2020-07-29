# -*- coding: utf-8 -*-
# app/auth/__init__.py

from flask import Blueprint

location = Blueprint('management.asset_location', __name__)

from . import views
