from odoo import models, fields, api
from odoo.exceptions import UserError

CORRPREV= [
    ('corr', 'Correctivo'),
    ('prev','Preventivo')
]

ODOHOR= [
    ('odo', 'Odómetro'),
    ('hor_tr', 'Horómetro Camión'),
    ('hor','Horómetro Grúa'),
    ('no','Sin valor')
]

class FleetVehicleLogServices(models.Model):
    _name = 'fleet.vehicle.log.services'
    _inherit = ['fleet.vehicle.log.services']
    _order = 'date desc'

    odometer_note = fields.Float(string="Odómetro")
    type_mant = fields.Selection(CORRPREV,string="Tipo servicio", default="corr")
    odo_hor = fields.Selection(ODOHOR,string="Selección Valor", default="odo")
    horometer_note = fields.Float(string="Horómetro")

    def make_external_service(self):
        for record in self:
            if record.odo_hor == 'odo'  :
                value = str(record.odometer_note) + ' km'
            elif record.odo_hor =='hor' or record.odo_hor == 'hor_tr':
                value = str(record.horometer_note) + ' hrs'
            else:
                value = False
            notes = record.notes
            project_id = self.env['project.project'].search([('is_fsm','=',True),('is_fsm_mantention','=',True)],limit=1)
            complete_name = record.description + ' - ' + record.vehicle_id.name
            if value:
                complete_name = complete_name + ' - ' + value
            description = "<p>Mantención de maquina " + record.vehicle_id.name + " por "+ dict(self._fields['odo_hor'].selection).get(record.odo_hor) + ": </p> <p>" + complete_name
            if notes:
                description = description + '.</p> <p>Notas:' +notes + '</p>'
            project_task_values = {
                'name':complete_name,
                'planned_date_begin': record.date,
                'description': description,
                'is_fsm':True,
                'project_id': project_id.id,
            }
            if record.vehicle_id.number_serie_id:
                project_task_values['number_serie_id'] = record.vehicle_id.number_serie_id.id
            record.state = 'running'
            project_task_values = self.env['project.task'].sudo().create(project_task_values)
            return True

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_todo(self):
        for record in self:
            record.state = "new"

    def write(self,values):
        res = super(FleetVehicleLogServices,self).write(values)
        for record in self:
            if 'state' not in values:
                if record.state != 'todo':
                    raise UserError('No puede modificar un servicio que no este por hacer.')
        return res
