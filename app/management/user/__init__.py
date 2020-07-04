# -*- coding: utf-8 -*-
# app/auth/__init__.py

from flask import Blueprint

user = Blueprint('management.user', __name__)

from . import views
