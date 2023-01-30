from odoo import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner']

    def _get_cheques(self,partner = False):
        if partner:
            cheques = self.env['account.bank.statement.line'].search([('partner_id', '=' ,partner.id),('journal_id.code', 'ilike' ,'CHC'),('is_reconciled','=',False)])
            return cheques
        return {}
