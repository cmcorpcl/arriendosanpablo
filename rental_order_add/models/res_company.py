from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResCompany(models.Model):
    _inherit = ['res.company']

    note_rental = fields.Text(string='Detalle Arriendo')
