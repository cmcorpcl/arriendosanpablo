# coding: utf-8
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cl_delivery_guide_price = fields.Selection([
        ('product', 'From Product'),
        ('sale_order', 'From Sale Order'),
        ('none', 'Do Not Show Price'),
        ('price','Precio Elegido')
    ], string='Delivery Guide Price', default='sale_order')

    l10n_cl_delivery_selected_price = fields.Float(string="Precio producto", default="0")