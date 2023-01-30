# -*- coding: utf-8 -*-
import logging


from odoo import models, fields, _, api
from odoo.tools import float_repr

_logger = logging.getLogger(__name__)

TAX19_SII_CODE = 14


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _l10n_cl_get_tax_amounts(self):
        """
        Calculates the totals of the tax amounts on the picking
        :return: totals, retentions, line_amounts
        """
        totals = {
                'vat_amount': 0,
                'subtotal_amount_taxable': 0,
                'subtotal_amount_exempt': 0,
                'vat_percent': False,
                'total_amount': 0,
            }
        retentions = {}
        line_amounts = {}
        sale_line = False
        guide_price = self.partner_id.l10n_cl_delivery_guide_price
        if guide_price == "none":
            return totals, retentions, line_amounts
        # No support for foreign currencies: fallback on product price
        if guide_price == "sale_order" and (
                not self.sale_id or self.sale_id.currency_id != self.company_id.currency_id):
            guide_price = "product"
        max_vat_perc = 0.0
        move_retentions = self.env['account.tax']
        for move in self.move_lines.filtered(lambda x: x.quantity_done > 0):
            if guide_price == "product" or not move.sale_line_id:
                taxes = move.product_id.taxes_id.filtered(lambda t: t.company_id == self.company_id)
                price = move.product_id.lst_price
                qty = move.product_qty
            elif guide_price == "sale_order":
                sale_line = move.sale_line_id
                taxes = sale_line.tax_id
                qty = move.product_uom._compute_quantity(move.product_uom_qty, sale_line.product_uom)
                price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) / 100.0)
            elif guide_price == "price":
                sale_line = move.sale_line_id
                taxes = sale_line.tax_id
                qty = move.product_uom._compute_quantity(move.product_uom_qty, sale_line.product_uom)
                price = self.partner_id.l10n_cl_delivery_selected_price if self.partner_id.l10n_cl_delivery_selected_price else 0

            tax_res = taxes.compute_all(
                price,
                currency=self.company_id.currency_id,
                quantity=qty,
                partner=self.partner_id
            )
            totals['total_amount'] += tax_res['total_included']

            no_vat_taxes = True
            for tax_val in tax_res['taxes']:
                tax = self.env['account.tax'].browse(tax_val['id'])
                if tax.l10n_cl_sii_code == TAX19_SII_CODE:
                    no_vat_taxes = False
                    totals['vat_amount'] += tax_val['amount']
                    max_vat_perc = max(max_vat_perc, tax.amount)
                elif tax.tax_group_id.id in [self.env.ref('l10n_cl.tax_group_ila').id, self.env.ref(
                        'l10n_cl.tax_group_retenciones').id]:
                    retentions.setdefault((tax.l10n_cl_sii_code, tax.amount), 0.0)
                    retentions[(tax.l10n_cl_sii_code, tax.amount)] += tax_val['amount']
                    move_retentions |= tax
            if no_vat_taxes:
                totals['subtotal_amount_exempt'] += tax_res['total_excluded']
            else:
                totals['subtotal_amount_taxable'] += tax_res['total_excluded']

            line_amounts[move] = {
                "value": self.company_id.currency_id.round(tax_res['total_included']),
                'total_amount': self.company_id.currency_id.round(tax_res['total_excluded']),
                "price_unit": self.company_id.currency_id.round(tax_res['total_excluded'] / move.product_uom_qty),
                "wh_taxes": move_retentions,
                "exempt": not taxes and tax_res['total_excluded'] != 0.0,
            }
            if guide_price == "sale_order" and sale_line:
                if sale_line.discount:
                    tax_res_disc = taxes.compute_all(
                        sale_line.price_unit,
                        currency=self.company_id.currency_id,
                        quantity=qty,
                        partner=self.partner_id
                    )
                    line_amounts[move].update({
                        'price_unit': self.company_id.currency_id.round(
                            tax_res_disc['total_excluded'] / move.product_uom_qty),
                        'discount': sale_line.discount,
                        'total_discount': float_repr(self.company_id.currency_id.round(tax_res_disc['total_excluded'] * sale_line.discount / 100), 0),
                        'total_discount_fl': self.company_id.currency_id.round(tax_res_disc['total_excluded'] * sale_line.discount / 100),
                    })

        totals['vat_percent'] = max_vat_perc and float_repr(max_vat_perc, 2) or False
        retention_res = []
        for key in retentions:
            retention_res.append({'tax_code': key[0],
                                  'tax_percent': key[1],
                                  'tax_amount': retentions[key]})
        return totals, retention_res, line_amounts

    def _l10n_cl_edi_prepare_values(self):
        move_lines = self.move_lines
        values = {
            'format_vat': self._l10n_cl_format_vat,
            'format_length': self._format_length,
            'time_stamp': self._get_cl_current_strftime(),
            'caf': self.l10n_latam_document_type_id.sudo()._get_caf_file(self.company_id.id,int(self.l10n_latam_document_number)),
            'fe_value': self.date_done.date(),
            'rr_value': '55555555-5' if self.partner_id._l10n_cl_is_foreign() else self._l10n_cl_format_vat(
                self.partner_id.vat),
            'rsr_value': self._format_length(self.partner_id.name, 40),
            'mnt_value': float_repr(self._l10n_cl_get_tax_amounts()[0]['total_amount'], 0),
            'picking': self,
            'it1_value': self._format_length(move_lines[0].product_id.name, 40) if move_lines else '',
        }
        return values