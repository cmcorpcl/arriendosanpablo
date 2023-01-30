from odoo import models, fields, api

class FuelOdometer(models.Model):
    _name = 'fuel.odometer'
    _rec_name = 'number'

    sale_id = fields.Many2one('sale.order',string="Pedido")
    number = fields.Float(string="Numero")
    fuel = fields.Float(string="Combustible")
    odometer = fields.Float(string="Odometro")