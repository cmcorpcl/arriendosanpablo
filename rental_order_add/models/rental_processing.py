from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RentalProcessingLine(models.TransientModel):
    _inherit = ['rental.order.wizard.line']
