
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    zone_stored = fields.Char(string="Zona destino")
    zone_name = fields.Char(string="Zona", stored=False, compute="_compute_zone")

    @api.depends("origin")
    def _compute_zone(self):
        for record in self:
            sale_env = self.env['sale.order'].search([('name',"=",record.origin)],limit=1)
            if sale_env:
                record.zone_name = sale_env.zone_id.name
                record.zone_stored = sale_env.zone_id.name
            else:
                record.zone_name = ""
                record.zone_stored = ""