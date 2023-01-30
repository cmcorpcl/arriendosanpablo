# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

OPTION = [
    ('Empleado','Empleado'),
    ('Nuevo','Nuevo')
]

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    option = fields.Selection(OPTION, string="Opción", default='Empleado')
    driver_id = fields.Many2one('hr.employee',string="Conductor asociado", domain="[('driver_ok','=',True)]")
    driver_id_vat = fields.Char(related='driver_id.identification_id', string="Rut asociado")
    driver_truck_id = fields.Many2one('guide.truck', related="driver_id.truck_id", string="Camión asociado")
    driver_truck_id_serial = fields.Char(related="driver_truck_id.truck_serial_number", string="Patente asociada")
    truck_id = fields.Many2one('guide.truck', string="Camión")
    truck_serial_number = fields.Char(related='truck_id.truck_serial_number',string="Patente")
    driver_name = fields.Char(string="Conductor")
    rut_driver = fields.Char(string="Rut de Conductor")
    picking_type_code = fields.Selection(related="picking_type_id.code")

    def write(self,vals):
        if 'option' in vals:
            for picking in self.picking_ids:
                picking.update({'option': vals['option']})
        else:
            for picking in self.picking_ids:
                picking.update({'option': self.option})
        if 'driver_id' in vals:
            for picking in self.picking_ids:
                picking.update({'driver_id': vals['driver_id']})
        else:
            for picking in self.picking_ids:
                picking.update({'driver_id': self.driver_id})
        if 'driver_name' in vals:
            for picking in self.picking_ids:
                picking.update({'driver_name': vals['driver_name']})
        else:
            for picking in self.picking_ids:
                picking.update({'driver_name': self.driver_name})
        if 'rut_driver' in vals:
            for picking in self.picking_ids:
                picking.update({'rut_driver': vals['rut_driver']})
        else:
            for picking in self.picking_ids:
                picking.update({'rut_driver': self.rut_driver})
        if 'truck_id' in vals:
            for picking in self.picking_ids:
                picking.update({'truck_id': vals['truck_id']})
        else:
            for picking in self.picking_ids:
                picking.update({'truck_id': self.truck_id})
        res = super(StockPickingBatch, self).write(vals)
        return res
