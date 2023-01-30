from locale import currency
from odoo import models, fields, api


STATE_SELECTION = [
    ('1', 'Recibido'),
    ('2', 'Diferencias'),
    ('3', 'Pendiente'),
]

class PurchaseLedgerInvoice(models.Model):
    _name = 'purchase.ledger.invoice'
    _description = 'Borrador de facturas de libro de compras'
    _rec_name = 'invoice_number'
    _order='state asc, date desc'

    invoice_number = fields.Char(string="Folio", required=True)
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    bussiness_line = fields.Char(string="Razón Social")
    invoice_rut = fields.Char(string="RUT", required=True)
    invoice_type = fields.Char(string="Tipo de Documento")
    invoice_type_code = fields.Char(string="Codigo")
    date = fields.Date(string="Fecha")
    net_amount = fields.Integer(string="Monto neto")
    tax_amount = fields.Integer(string="Monto impuesto")
    exnt_amount = fields.Integer(string='Monto Exento')
    total_amount = fields.Integer(string="Total")
    state = fields.Selection(STATE_SELECTION, string="Estado")
    invoice_id = fields.Many2one('account.move', string="Factura")
    currency_id = fields.Many2one('res.currency', string='Moneda')
    invoice_total = fields.Monetary(related="invoice_id.amount_total", string="Total Factura")
    company_id = fields.Many2one("res.company", string="Compañia", default=lambda self: self.env.company)

    def create_invoice(self):
        net = self.net_amount
        if self.invoice_type_code == "34":
            net = self.exnt_amount
        partner =  self.partner_id
        if not self.partner_id:
            partner = self.env['res.partner'].search([('vat','=',self.invoice_rut)])
        return  {
                'name': 'Crear Factura',
                'view_mode':'form',
                'view_type':'form',
                'res_model':'purchase_ledger.create_invoice.wizard',
                'views': [(self.env.ref('purchase_ledger_sii.view_create_purchase_invoice_form').id, 'form')],
                'context': {
                    'default_partner_id': partner.id,
                    'default_bussiness_line': self.bussiness_line,
                    'default_date':self.date,
                    'default_invoice_rut': self.invoice_rut,
                    'default_invoice_number': self.invoice_number,
                    'default_total': self.total_amount,
                    "default_purchase_ledger_invoice": self.id,
                    "default_invoice_type_code":self.invoice_type_code,
                    "default_company_id":self.company_id.id,
                    "default_net_amount":net,
                },
                'type':'ir.actions.act_window',
                'target': 'new',
        }
