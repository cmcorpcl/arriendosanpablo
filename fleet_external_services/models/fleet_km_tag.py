from odoo import _,models, fields, api

class FleetKmTag(models.Model):
    _name = 'fleet.km.tag'

    name = fields.Char(string="Nombre de etiqueta")