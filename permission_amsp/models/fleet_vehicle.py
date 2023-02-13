from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    def copy_to_rental(self):
        res = super(FleetVehicle,self).copy_to_rental()
        if  not self.env.user.fleet_to_rental_right:
            raise UserError('Este usuario no presenta permisos para traspaso de datos a arriendo.')
        return res

"""     def write(self,vals):
        res = super(FleetVehicle,self).write(vals)
        if not self.env.user.fleet_edit:
            raise UserError('Este usuario no presenta permisos para la edición de flota.')
        return res """