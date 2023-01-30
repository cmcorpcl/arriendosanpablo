from odoo import models, fields, api

class ResPartnerCategory(models.Model):
    _inherit = ['res.partner.category']

    is_bot_mantention = fields.Boolean(string="¿Es bot de mantención?")
