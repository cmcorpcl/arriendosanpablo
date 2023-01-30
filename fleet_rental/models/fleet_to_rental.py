from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicle(models.TransientModel):
    _name = 'fleet.to.rental'

    rental_id = fields.Many2one('sale.order', string='Arriendo Asociado',domain="[('is_rental_order','=',True),('fleet_id','=',False)]")
    fleet_id = fields.Many2one('fleet.vehicle',string="Flota",required="1")


    def action_copy(self):
        for record in self:
            if record.rental_id:
                record.rental_id.write({
                    'tonnage': record.fleet_id.tonnage if record.fleet_id.tonnage else 0,
                    'driver_id': record.fleet_id.driver_id.id if  record.fleet_id.driver_id else False,
                    'fleet_id':record.fleet_id.id
                })
            else:
                raise UserError('No se ingreso un arriendo a asociar.')
