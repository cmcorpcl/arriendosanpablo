from odoo import models, fields, api

class FleetVehicleModel(models.Model):
    _name = 'fleet.vehicle.model'
    _inherit = ['fleet.vehicle.model']

    km_ids = fields.One2many('fleet.model.km','model_id',string="Kilometraje a mantención")
    truck_horometer_ids = fields.One2many('fleet.model.horometer','truck_model_id',string="Horómetro Camión a mantención")
    crane_horometer_ids = fields.One2many('fleet.model.horometer','crane_model_id',string="Horómetro Grúa a mantención")
