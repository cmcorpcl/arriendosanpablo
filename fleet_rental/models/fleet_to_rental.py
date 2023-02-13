from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetToVehicle(models.TransientModel):
    _name = 'fleet.to.rental'

    rental_id = fields.Many2one('sale.order', string='Arriendo Asociado',domain="[('is_rental_order','=',True),('fleet_id','=',False)]")
    fleet_id = fields.Many2one('fleet.vehicle',string="Flota",required="1")
    operator_id = fields.Many2one('hr.employee', string="Operator", domain="[('operator_ok','=',True)]")
    rigger_id = fields.Many2one('hr.employee', string="Rigger", domain="[('rigger_ok','=',True)]")
    driver_id = fields.Many2one('res.partner', string="Conductor")
    needs_rigger = fields.Boolean(string="¿Necesita Rigger?")
    needs_operator = fields.Boolean(string="¿Necesita Operador?")


    def action_copy(self):
        for record in self:
            if record.fleet_id:
                if record.operator_id:
                    record.fleet_id.sudo().update({'operator_id': record.operator_id.id})
                    if record.operator_id.partner_id:
                        record.fleet_id.sudo().update({'driver_id':  record.operator_id.partner_id.id})
                if record.rigger_id:
                    record.fleet_id.sudo().update({'rigger_id': record.rigger_id.id})
            if record.rental_id:
                record.rental_id.sudo().write({
                    'tonnage': record.fleet_id.tonnage if record.fleet_id.tonnage else 0,
                    'operator_id': record.fleet_id.operator_id.id if record.fleet_id.operator_id else False,
                    'rigger_id': record.fleet_id.rigger_id.id if record.fleet_id.rigger_id else False,
                    'driver_id': record.fleet_id.driver_id.id if  record.fleet_id.driver_id else False,
                    'fleet_id':record.fleet_id.id,
                })
            else:
                raise UserError('No se ingreso un arriendo a asociar.')
