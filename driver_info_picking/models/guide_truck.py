# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class GuideTruck(models.Model):
    _name = "guide.truck"
    _rec_name = "truck_serial_number"

    truck_serial_number = fields.Char(string="Patente",required=True )
    model = fields.Char(string="Modelo")
    code = fields.Char(string="Código")
