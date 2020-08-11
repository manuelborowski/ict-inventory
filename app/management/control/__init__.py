# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

control = Blueprint('management.control', __name__)

from . import views