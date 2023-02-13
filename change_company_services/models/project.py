from odoo import models, fields, api

class Project(models.Model):
    _inherit = ['project.project']

    companie_related_project_ids = fields.Many2many('project.project','project_rel_for_change','project_id1','project_id2',string="Projectos relacionados de otras compañias")
