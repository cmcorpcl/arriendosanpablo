from odoo import models, fields, api

class CLAcountInvoiceReference(models.Model):
    _name = 'l10n_cl.account.invoice.reference'
    _inherit = 'l10n_cl.account.invoice.reference'

    delivery_guide_id = fields.Many2one('stock.picking', string="Guia de despacho"  )
