from odoo import models, fields, api

class FleetVehicleLicense(models.Model):
    _name = 'fleet.vehicle.license'

    name = fields.Char(string="Matrícula")
