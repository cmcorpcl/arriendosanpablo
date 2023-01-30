from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    days_plus_default = fields.Boolean()
    days_to_sum = fields.Integer()
