from odoo import models, fields, api

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    def change_company_from_wizard(self):
        for record in self:
            return  {
                'name': 'Cambiar compañia de venta/alquiler',
                'view_mode':'form',
                'view_type':'form',
                'res_model':'change.sale.company',
                'views': [(self.env.ref('change_company_services.change_sale_order_company_form').id, 'form')],
                'context': {
                    'default_sale_order_id': record.id,
                },
                'type':'ir.actions.act_window',
                'target': 'new',
        }
