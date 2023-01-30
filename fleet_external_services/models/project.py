from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = ['project.project']

    is_fsm_mantention = fields.Boolean(string="¿Se ocupa para mantención?")
