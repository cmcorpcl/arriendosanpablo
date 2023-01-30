# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class RentalProcessingLine(models.TransientModel):
    _inherit = 'rental.order.wizard.line'

    maintance_lot_ids = fields.Many2many('stock.production.lot', 'wizard_maintance_serial', store=False)

    def _default_wizard_line_vals(self, line, status):
        default_line_vals = super(RentalProcessingLine, self)._default_wizard_line_vals(line, status)
        maintance_ids = self.env['stock.production.lot'].sudo().search([('is_in_maintance','=',True)])
        default_line_vals.update({
            'maintance_lot_ids': [(6, 0, maintance_ids.ids)],
        })
        print(default_line_vals)
        return default_line_vals

    pickedup_lot_ids = fields.Many2many('stock.production.lot', 'wizard_pickedup_serial',domain="[('id', 'in', pickeable_lot_ids),('id','not in',maintance_lot_ids)]")