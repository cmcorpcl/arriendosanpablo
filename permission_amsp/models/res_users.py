from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    fleet_to_rental_right = fields.Boolean(string="Permiso asociación maquina a alquiler", help="Permiso para asociar maquina con una alquiler")
    pick_rental_right = fields.Boolean(string="Permiso de recogida/devolución de maquina", help="Permiso para la recogida de una maquina en alquiler")
    edit_rental = fields.Boolean(string="Permiso edición alquiler", help="Permiso para editar un alquiler (Menos datos de flota)")
    fleet_edit = fields.Boolean(string="Permisos edición Flota")
    fuel_edit = fields.Boolean(string="Permiso edición lista de combustible")
    odometer_edit = fields.Boolean(string="Permiso edición lista de odometro")
