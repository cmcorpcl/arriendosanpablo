from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RentalChor(models.Model):
    _name = 'rental.chor'
    _description = 'Mantenedor de Faena'
    _rec_name = 'name'

    name = fields.Char(string="Nombre")
