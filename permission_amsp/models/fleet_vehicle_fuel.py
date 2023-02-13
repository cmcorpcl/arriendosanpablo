from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicleFuel(models.Model):
    _inherit = 'fleet.vehicle.fuel'

    def write(self,vals):
        res = super(FleetVehicleFuel,self).write(vals)
        if  not self.env.user.fuel_edit:
            raise UserError('Este usuario no presenta permisos para la edición de combustible.')
        return res