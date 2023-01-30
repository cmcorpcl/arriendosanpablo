from odoo import models, fields, api

class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    product_template_amsp = fields.Boolean(string="¿Es un template para AMSP?")
