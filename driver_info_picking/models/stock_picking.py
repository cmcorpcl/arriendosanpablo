# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

OPTION = [
    ('Empleado','Empleado'),
    ('Nuevo','Nuevo')
]

class StockPicking(models.Model):
    _inherit = "stock.picking"

    option = fields.Selection(OPTION, string="Opción", default='Empleado')
    driver_id = fields.Many2one('hr.employee',string="Conductor asociado", domain="[('driver_ok','=',True)]")
    driver_id_vat = fields.Char(related='driver_id.identification_id', string="Rut asociado")
    driver_truck_id = fields.Many2one('guide.truck', related="driver_id.truck_id", string="Camión asociado")
    driver_truck_id_serial = fields.Char(related="driver_truck_id.truck_serial_number", string="Patente asociada")
    truck_id = fields.Many2one('guide.truck', string="Truck")
    truck_serial_number = fields.Char(related='truck_id.truck_serial_number',string="Patente")
    driver_name = fields.Char(string="Conductor")
    rut_driver = fields.Char(string="Rut de Conductor")
    zone_stored = fields.Char(string="Zona destino")
    zone_name = fields.Char(string="Zona", stored=False, compute="_compute_zone")

    @api.depends("origin")
    def _compute_zone(self):
        for record in self:
            sale_env = self.env['sale.order'].search([('name',"=",record.origin)],limit=1)
            if sale_env:
                record.zone_name = sale_env.zone_id.name
                record.zone_stored = sale_env.zone_id.name
            else:
                record.zone_name = ""
                record.zone_stored = ""

    @api.onchange('batch_id')
    def _onchange_batch_id_driver(self):
        for record in self:
            if record.batch_id:
                record.option = record.batch_id.option
                record.driver_id = record.batch_id.driver_id
                record.driver_name = record.batch_id.driver_name
                record.rut_driver = record.batch_id.rut_driver
                record.truck_id = record.batch_id.truck_id
