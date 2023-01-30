# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    driver_ok = fields.Boolean(string="¿Este empleado es conductor?")
    truck_id = fields.Many2one('guide.truck', string="Patente Camión")