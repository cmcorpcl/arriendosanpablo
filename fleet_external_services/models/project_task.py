from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = ['project.task']

    number_serie_id = fields.Many2one('stock.production.lot',string="Lote/Numero de serie en mantención")

    def write(self,values):
        res = super(ProjectTask,self).write(values)
        for record in self:
            print(values)
            if 'stage_id' in values:
                project_type_task = self.env['project.task.type'].sudo().search([('id','=',values['stage_id'])],limit=1)
                print(project_type_task)
                print(project_type_task.is_maintance)
                print(project_type_task.is_done_maintance)
                if project_type_task and project_type_task.is_maintance:
                    if 'number_serie_id' in values:
                        serie_id = self.env['stock.production.lot'].sudo().search([('id','=',values['number_serie_id'])],limit=1)
                        print(serie_id)
                        if serie_id:
                            serie_id.sudo().write({'is_in_maintance':True})
                        elif record.number_serie_id:
                            record.number_serie_id.sudo().write({'is_in_maintance':True})
                    elif record.number_serie_id:
                        record.number_serie_id.sudo().write({'is_in_maintance':True})
                if project_type_task and project_type_task.is_done_maintance:
                    if 'number_serie_id' in values:
                        serie_id = self.env['stock.production.lot'].sudo().search([('id','=',values['number_serie_id'])],limit=1)
                        if serie_id:
                            serie_id.sudo().write({'is_in_maintance':False})
                        elif record.number_serie_id:
                            record.number_serie_id.sudo().write({'is_in_maintance':False})
                    elif record.number_serie_id:
                        record.number_serie_id.sudo().write({'is_in_maintance':False})
        return res


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_maintance = fields.Boolean(string="¿Etapa de mantenimiento?")
    is_done_maintance = fields.Boolean(string="¿Etapa de termino de mantención?")
