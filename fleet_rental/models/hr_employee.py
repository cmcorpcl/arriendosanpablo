# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    rigger_ok = fields.Boolean(string="¿Este empleado es rigger?")
    operator_ok = fields.Boolean(string="¿Este empleado es operador?")
    amsp_partner_id = fields.Many2one('res.partner',string="Contacto AMSP")