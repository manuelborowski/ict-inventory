from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.widgets import HiddenInput


class EditForm(FlaskForm):
    name = StringField('Naam')
    info = StringField('Info')
    standards = StringField('Norm(en)')
    active = BooleanField('Actief')
    id = IntegerField(widget=HiddenInput())

class AddForm(EditForm):
    pass

class ViewForm(FlaskForm):
    name = StringField('Naam', render_kw={'readonly':''})
    info = StringField('Info', render_kw={'readonly':''})
    standards = StringField('Norm(en)', render_kw={'readonly':''})
    active = BooleanField('Actief', render_kw={'disabled':''})
    id = IntegerField(widget=HiddenInput())
