from odoo import models, fields, api

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def make_l10n_ch_guide_pickings(self):
        self.ensure_one()
        for picking in self.picking_ids:
            picking.create_delivery_guide()
        return self.env.ref('l10n_cl_edi_stock.action_delivery_guide_report_pdf').report_action(self.picking_ids)

    def print_delivery_guide_pdf(self):
        self.ensure_one()
        return self.env.ref('l10n_cl_edi_stock.action_delivery_guide_report_pdf').report_action(self.picking_ids)
