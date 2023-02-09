from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    def open_pickup(self):
        res = super(SaleOrder,self).open_pickup()
        if not self.env.user.pick_rental_right:
            raise UserError('Este usuario no presenta permisos para recogida.')
        return res

    def open_return(self):
        res = super(SaleOrder,self).open_return()
        if not self.env.user.pick_rental_right:
            raise UserError('Este usuario no presenta permisos para la devolución.')
        return res

    def write(self,vals):
        res = super(SaleOrder,self).write(vals)
        for record in self:
            values_list = ['tonnage','driver_id','fleet_id','rigger_id','operator_id']
            if  not self.env.user.pick_rental_right:
                for value in values_list:
                    if value in vals:
                        raise UserError('No tiene permiso para modificar datos de flota en alquiler.')
        return res