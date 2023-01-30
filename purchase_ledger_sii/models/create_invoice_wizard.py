
import json
from odoo import models, fields, api
import datetime
from requests import Session
from odoo.exceptions import UserError

class CreateInvoiceWizard(models.TransientModel):
    _name = 'purchase_ledger.create_invoice.wizard'
    _description = 'Crear factura a traves de la sincronización del libro de compra'

    partner_id = fields.Many2one('res.partner', string='Proveedor', required=True)
    bussiness_line = fields.Char(string="Razón social")
    date = fields.Date(string="Fecha")
    invoice_number = fields.Char(string="Folio")
    invoice_rut = fields.Char(string="RUT")
    invoice_type_code = fields.Char(string="Tipo de factura")
    total = fields.Integer(string="Total")
    net_amount = fields.Float(string="Neto")
    purchase_ledger_invoice = fields.Many2one('purchase.ledger.invoice', string="Factura de libro de compra")
    company_id = fields.Many2one('res.company', string="Compañia")


    def create_invoice_from_ledger(self):
        account_move_env = self.env['account.move']
        tax_id_iva = self.env['account.tax'].search([('name','ilike',"iva")],limit=1)
        print(tax_id_iva)
        print(tax_id_iva.name) if tax_id_iva else print('No hay')
        invoice_info = {
            'invoice_date': self.date,
            'date': self.date,
            'move_type': 'in_invoice',
            'sequence_number': self.invoice_number,
            'l10n_latam_document_number': self.invoice_number,
            'invoice_ledger_id': self.purchase_ledger_invoice.id,
            'invoice_ledger_total': self.total,
            'state': 'draft',
            'company_id':self.company_id.id,
            'invoice_line_ids': [(0,0,{
                "name": 'Factura SII',
                "quantity": 1,
                "price_unit": self.net_amount,
                "tax_ids": [(4,tax_id_iva.id)] if tax_id_iva and self.invoice_type_code == "33"  else []
            })],
        }
        partner_encounter = self.env['res.partner'].search([('id','=',self.partner_id.id)])
        if len(partner_encounter) > 0:
            invoice_info['partner_id'] = partner_encounter[0].id
        document_type_encounter = self.env['l10n_latam.document.type'].search([('code','=', self.invoice_type_code)])
        if len(document_type_encounter) > 0:
            invoice_info['l10n_latam_document_type_id'] = document_type_encounter[0].id
        account_values = account_move_env.create(invoice_info)
        purchase_ledger_env = self.env['purchase.ledger.invoice']
        purchase_ledger_encounter = purchase_ledger_env.search([('id','=',self.purchase_ledger_invoice.id)], limit=1 )
        purchase_ledger_encounter.write({'state': '2', 'invoice_id': account_values.id})
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        form_view = [(self.env.ref('account.view_move_form').id, 'form')]
        if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                action['res_id'] = account_values.id
                return action
        return  {
            'name': 'Facturas',
            'view_mode':'tree,kanban,form',
            'view_type':'form',
            'res_model':'account.move',
            'views': [(self.env.ref('account.view_out_invoice_tree').id, 'tree'),
                      (self.env.ref('account.view_account_move_kanban').id, 'kanban'),
                      (self.env.ref('account.view_move_form').id, 'form')],
            'type':'ir.actions.act_window',
            'target': 'main',
            'nodestroy': True
        }
