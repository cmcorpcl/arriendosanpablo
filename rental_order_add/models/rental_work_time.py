from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RentalWorkTime(models.Model):
    _name = 'rental.work.time'
    _description = 'Jornada laboral de un alquiler'
    _rec_name = 'name'

    name = fields.Char(string="Nombre")
