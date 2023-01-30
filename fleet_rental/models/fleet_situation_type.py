from odoo import models, fields, api

class FleetSituationType(models.Model):
    _name = 'fleet.situation.type'


    name = fields.Char(string="Nombre")
    is_entry = fields.Boolean(string="¿Es entrada?")
    is_exit = fields.Boolean(string="¿Es salida?")
