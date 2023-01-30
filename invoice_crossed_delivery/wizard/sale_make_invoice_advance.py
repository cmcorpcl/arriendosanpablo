from itertools import product
from time import strftime
from odoo import models, fields, api, _
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        delivery_guides = self.env['stock.picking'].search([('l10n_latam_document_number','!=',False),('sale_id','=',order.id),('invoice_union_id','=',False),('state','=','done')])
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
            'ref': order.client_order_ref,
            'move_type': 'out_invoice',
            'invoice_origin': order.name,
            'invoice_user_id': order.user_id.id,
            'narration': order.note,
            'partner_id': order.partner_invoice_id.id,
            'fiscal_position_id': (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(order.partner_id.id)).id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'currency_id': order.pricelist_id.currency_id.id,
            'payment_reference': order.reference,
            'invoice_payment_term_id': order.payment_term_id.id,
            'partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
            'team_id': order.team_id.id,
            'campaign_id': order.campaign_id.id,
            'medium_id': order.medium_id.id,
            'source_id': order.source_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': so_line.product_uom.id,
                'tax_ids': [(6, 0, so_line.tax_id.ids)],
                'sale_line_ids': [(6, 0, [so_line.id])],
                'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                'analytic_account_id': order.analytic_account_id.id or False,
            })],
            'l10n_cl_reference_ids':[(6, 0, del_list)],
        }
        return invoice_vals
