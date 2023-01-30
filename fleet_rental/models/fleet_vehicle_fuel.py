from odoo import models, fields, api

class FleetVehicleFuel(models.Model):
    _name = 'fleet.vehicle.fuel'
    _order = 'date desc, time desc'

    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehiculo")
    driver_id = fields.Many2one('res.partner',string="Responsable de carga")
    date = fields.Date(string="Fecha", default=fields.Date.context_today)
    time = fields.Float(string="Tiempo")
    start_fuel = fields.Float(string="Kilometro de carga")
    end_fuel = fields.Float(string="Litros Cargados")
    note = fields.Char(string="Nota")
    rental_id = fields.Many2one('sale.order',string="Arriendo asociado", domain="[('is_rental_order','=',True)]")
