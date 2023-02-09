from odoo import models, fields, api

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    fleet_vehicle_fuel_ids = fields.One2many('fleet.vehicle.fuel','rental_id', string="Combustible")
    fleet_vehicle_odometer_ids = fields.One2many('fleet.vehicle.odometer','rental_id', string="Odomentro")
    tonnage=  fields.Char(string="Tonelaje",copy=False)
    driver_id = fields.Many2one('res.partner',string="Conductor",copy=False)
    fleet_id = fields.Many2one('fleet.vehicle',string="Flota",copy=False)
    rigger_id = fields.Many2one('hr.employee', string="Rigger", copy=False)
    operator_id = fields.Many2one('hr.employee', string="Operario", copy=False)
