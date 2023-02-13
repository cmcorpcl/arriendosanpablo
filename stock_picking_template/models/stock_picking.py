
from odoo import SUPERUSER_ID, api, fields, models, _
from odoo.tools import is_html_empty

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    picking_template_id = fields.Many2one('stock.picking.template',string="Elegir Plantilla")
    template_sum = fields.Boolean(string="Se suman los productos de la plantilla?", default=False)

    @api.onchange('picking_template_id')
    def onchange_picking_template_id(self):
        for record in self:
            if record.picking_template_id:
                template = record.picking_template_id
                record.move_ids_without_package = [(5,0,0)]
                list_data = []
                for line in template.stock_template_line_ids:
                    data={
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.product_id.uom_id.id
                    }
                    #record.sudo().write({'move_ids_without_package': [(0,0,data)]})
                    list_data.append((0,0,data))
                record.move_ids_without_package = list_data
