from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    template_product = fields.Many2one('ir.ui.view',string="Template",domain=[('type','=','qweb'),('product_template_amsp','=',True)])
    tonnage_id = fields.Many2one('product.tonnage',string="Tonelaje Sugerido")

    @api.onchange('product_id')
    def _onchange_product_id_amsp(self):
        for record in self:
            if record.product_id and record.product_id.template_quotation:
                record.template_product = record.product_id.template_quotation
            else:
                record.template_product = False
