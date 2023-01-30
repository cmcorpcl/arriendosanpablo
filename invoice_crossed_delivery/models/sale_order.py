from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'


    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))
        delivery_guides = self.env['stock.picking'].search([('l10n_latam_document_number','!=',False),('sale_id','=',self.id),('invoice_union_id','=',False),('state','=','done')])
        print('SE INGRESO A ESTA PARTE')
        del_list=[]
        for delivery in delivery_guides:
            del_ref = {
                "delivery_guide_id": delivery.id,
                "origin_doc_number": str(delivery.l10n_latam_document_number),
                "l10n_cl_reference_doc_type_selection": delivery.l10n_latam_document_type_id.code,
                "date": delivery.date_done
            }
            ref_done = self.env['l10n_cl.account.invoice.reference'].create(del_ref)
            del_list.append(ref_done.id)
        print(del_list)
        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
            'l10n_cl_reference_ids':[(6, 0, del_list)],
            'picking_ref_ids':[(6,0,delivery_guides.ids)]
        }
        return invoice_vals
