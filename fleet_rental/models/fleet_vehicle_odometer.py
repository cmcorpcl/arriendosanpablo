from odoo import models, fields, api

class FleetVehicleOdometer(models.Model):
    _name = 'fleet.vehicle.odometer'
    _inherit = ['fleet.vehicle.odometer']
    _order = 'date desc, time desc'

    time = fields.Float(string='Tiempo')
    situation_type_id = fields.Many2one('fleet.situation.type',string="Tipo de registro")
    rental_id = fields.Many2one('sale.order', string='Arriendo Asociado',domain="[('is_rental_order','=',True)]")
    note = fields.Char(string="Nota")
