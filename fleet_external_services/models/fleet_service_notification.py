from odoo import _,models, fields, api

class FleetServiceNotification(models.Model):
    _name = 'fleet.service.notification'
    _order = 'date desc'

    date = fields.Datetime(string="Fecha", readonly=True)
    number = fields.Integer(string="N° Aviso", readonly=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehiculo",readonly=True )
    notification = fields.Text(string="Aviso",readonly=True)