# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"

    zone_id = fields.Many2one("destination.zone", string="Zona destino")