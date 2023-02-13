from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = ['account.analytic.line']

    report_number = fields.Integer(string="Numero de reporte")
    note = fields.Float(string="Horas de trabajo")