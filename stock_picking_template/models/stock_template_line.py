
from odoo import SUPERUSER_ID, api, fields, models, _

class StockPickingTemplateLine(models.Model):
    _name = 'stock.picking.template.line'
    _rec_name = 'product_id'

    template_id = fields.Many2one('stock.picking.template',string="Template")
    product_id = fields.Many2one('product.product',string="Producto")
    quantity = fields.Float(string="Cantidad")
