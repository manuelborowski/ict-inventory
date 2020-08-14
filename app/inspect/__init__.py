# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

inspect = Blueprint('inspect', __name__)

from . import views
