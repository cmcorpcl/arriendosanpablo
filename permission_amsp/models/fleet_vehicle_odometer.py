from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    def write(self,vals):
        res = super(FleetVehicleOdometer,self).write(vals)
        if  not self.env.user.odometer_edit:
            raise UserError('Este usuario no presenta permisos para la edición de odómetro.')
        return res
