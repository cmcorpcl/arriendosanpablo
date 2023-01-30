# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    zone_id = fields.Many2one('destination.zone', compute="_onchange_partner_shipping_zone_id" ,string="Zona destino")

    @api.depends('partner_id', 'partner_shipping_id')
    def _onchange_partner_shipping_zone_id(self):
        for record in self:
            record.zone_id = record.partner_id.zone_id
            if record.partner_shipping_id and record.partner_shipping_id.zone_id:
                record.zone_id = record.partner_shipping_id.zone_id
