from odoo import models, fields, _, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_order_ref = fields.Char(string='Customer Reference', copy=False, size=18)

    @api.onchange('client_order_ref')
    def _validate_order_ref(self):
        for record in self:
            sale_with_equal = self.env['sale.order'].search(['&','|',('partner_id','=',record.partner_id.id),('partner_invoice_id','=',record.partner_id.id),('client_order_ref','=',record.client_order_ref),('name','!=',record.name)], limit=1)
            if sale_with_equal:
                if sale_with_equal.partner_id == sale_with_equal.partner_invoice_id:
                    if sale_with_equal.partner_id  == record.partner_id:
                        raise UserError('Esta referencia de compra ya existe en el pedido {} del cliente {}'.format(sale_with_equal.name,sale_with_equal.partner_id.name))
                else:
                    if sale_with_equal.partner_invoice_id  == record.partner_id:
                        raise UserError('Esta referencia de compra ya existe en el pedido {} del cliente {}'.format(sale_with_equal.name,sale_with_equal.partner_invoice_id.name))
