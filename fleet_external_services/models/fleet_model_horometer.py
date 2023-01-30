from odoo import _,models, fields, api

class FleetModelHorometer(models.Model):
    _name = 'fleet.model.horometer'

    crane_model_id = fields.Many2one('fleet.vehicle.model',string="Modelo Grúa")
    truck_model_id = fields.Many2one('fleet.vehicle.model',string="Modelo Camión")
    horometer = fields.Float(string="Horómetro")
    tags_ids = fields.Many2many('fleet.km.tag', string="Sugerencias")
    counter_mantention = fields.Float(string='Contador de avisos',readonly=True ,default=0)