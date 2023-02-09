
from odoo import SUPERUSER_ID, api, fields, models, _

class StockPickingTemplate(models.Model):
    _name = 'stock.picking.template'
    _rec_name = 'name'

    name = fields.Char(string="Nombre")
    stock_template_line_ids = fields.One2many('stock.picking.template.line','template_id',string='Lineas de Plantilla')
