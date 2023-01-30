# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError


class StockPickingToBatch(models.TransientModel):
    _inherit = 'stock.picking.to.batch'

    def attach_pickings(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].browse(self.env.context.get('active_ids'))
        if self.mode == 'new':
            company = pickings.company_id
            if len(company) > 1:
                raise UserError(_("The selected pickings should belong to an unique company."))
            batch = self.env['stock.picking.batch'].create({
                'user_id': self.user_id.id,
                'company_id': company.id,
                'picking_type_id': pickings[0].picking_type_id.id,
            })
        else:
            batch = self.batch_id

        pickings.write({'batch_id': batch.id})
        if self.mode != "new":
            pickings.write({
                'option': batch.option,
                'driver_id': batch.driver_id,
                'driver_name': batch.driver_name,
                "rut_driver": batch.rut_driver,
                "truck_id": batch.truck_id
                })