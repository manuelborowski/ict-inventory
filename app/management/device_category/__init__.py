# -*- coding: utf-8 -*-
# app/auth/__init__.py

from flask import Blueprint

category = Blueprint('management.device_category', __name__)

from . import views
