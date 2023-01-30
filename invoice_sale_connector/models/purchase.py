from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoice_connect_ids = fields.One2many('account.move','purchase_connect_ids', string='Facturas Asociadas')
