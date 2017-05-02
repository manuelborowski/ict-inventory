# -*- coding: utf-8 -*-
#app/suppliers/forms.py

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    """
    Edit an existing supplier
    """

    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')


class AddForm(EditForm):
    """
    Add a supplier
    """

