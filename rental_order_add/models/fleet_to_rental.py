from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicle(models.TransientModel):
    _inherit = 'fleet.to.rental'

    @api.onchange('rental_id')
    def _onchange_rental_id(self):
        for record in self:
            record.needs_operator = False
            record.needs_rigger = False
            if record.rental_id.work_operator == "yes":
                record.needs_operator = True
                if record.fleet_id and record.fleet_id.operator_id:
                    record.operator_id = record.fleet_id.operator_id
            if record.rental_id.work_rigger == "yes":
                record.needs_rigger = True
                if record.fleet_id and record.fleet_id.rigger_id:
                    record.rigger_id = record.fleet_id.rigger_id
            if record.fleet_id.driver_id:
                record.driver_id = record.fleet_id.driver_id

    def action_copy(self):
        for record in self:
            message = ""
            if record.fleet_id:
                message = "Se ha asociado la maquina "+ record.fleet_id.name
                if record.operator_id:
                    record.fleet_id.sudo().update({'operator_id': record.operator_id.id})
                    message = message + ' | Con el operador: ' + record.operator_id.name
                    if record.operator_id.amsp_partner_id:
                        record.fleet_id.sudo().update({'driver_id':  record.operator_id.amsp_partner_id.id})
                else:
                    record.fleet_id.sudo().update({'driver_id': False})
                if record.rigger_id:
                    record.fleet_id.sudo().update({'rigger_id': record.rigger_id.id})
                    message = message + ' | Con el rigger: ' + record.rigger_id.name
            if record.rental_id:
                record.rental_id.sudo().write({
                    'tonnage': record.fleet_id.tonnage if record.fleet_id.tonnage else 0,
                    'operator_id': record.fleet_id.operator_id.id if record.fleet_id.operator_id else False,
                    'rigger_id': record.fleet_id.rigger_id.id if record.fleet_id.rigger_id else False,
                    'driver_id': record.fleet_id.driver_id.id if  record.fleet_id.driver_id else False,
                    'fleet_id':record.fleet_id.id,
                    'state_rental_asp_store': 'orden_de_trabajo'
                })
                record.rental_id.sudo().message_post(body=message)
            else:
                raise UserError('No se ingreso un arriendo a asociar.')
