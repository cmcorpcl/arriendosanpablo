from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    days_plus_default = fields.Boolean(
        string="Dias predeterminados para fecha de venta" , related="company_id.days_plus_default", readonly=False,
        help="Activar dias de suma a fecha de venta" )
    days_to_sum = fields.Integer(
        string="Dias a sumar", related="company_id.days_to_sum", readonly=False,
        help="Numero de días a sumar en fecha"
    )