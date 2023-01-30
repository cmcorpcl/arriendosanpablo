import json
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_ledger_id = fields.Many2one('purchase.ledger.invoice', string='Factura SII')
    invoice_ledger_total = fields.Integer(string="Monto Total Factura SII", related="invoice_ledger_id.total_amount")



    def unlink(self):
        for record in self:
            if record.invoice_ledger_id:
                purchase_ledger_env = self.env['purchase.ledger.invoice']
                purchase_encounter =  purchase_ledger_env.search([('id', '=', record.invoice_ledger_id.id)], limit=1)
                if len(purchase_encounter) > 0:
                    purchase_encounter.write({'state':'3','invoice_id': False})
        return super(AccountMove, self).unlink()

    def write(self, vals):
        for record in self:
            if 'line_ids' in vals:
                total = 0
                for lines in vals['line_ids'][0]:
                    if isinstance(lines, dict):
                        for key,value in lines.items():
                            if key == "credit":
                                total += value
                if record.invoice_ledger_id:
                    if total != record.invoice_ledger_id.total_amount:
                        record.invoice_ledger_id.update({'state':'2'})
                    else:
                        record.invoice_ledger_id.update({'state':'1'})
        res = super(AccountMove,self).write(vals)
        return res
