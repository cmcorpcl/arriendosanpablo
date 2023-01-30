from odoo import _,models, fields, api

class FleetModelKM(models.Model):
    _name = 'fleet.model.km'

    model_id = fields.Many2one('fleet.vehicle.model',string="Modelo")
    km = fields.Float(string="KM")
    tags_ids = fields.Many2many('fleet.km.tag', string="Sugerencias")
    counter_mantention = fields.Float(string='Contador de avisos',readonly=True ,default=0)