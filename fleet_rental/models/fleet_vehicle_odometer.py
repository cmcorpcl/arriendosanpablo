from odoo import models, fields, api
from datetime import datetime

class FleetVehicleOdometer(models.Model):
    _name = 'fleet.vehicle.odometer'
    _inherit = ['fleet.vehicle.odometer']
    _order = 'date desc'

    date = fields.Datetime(string='Fecha', default=datetime.today())
    time = fields.Float(string='Tiempo')
    situation_type_id = fields.Many2one('fleet.situation.type',string="Tipo de registro")
    rental_id = fields.Many2one('sale.order', string='Arriendo Asociado',domain="[('is_rental_order','=',True)]")
    note = fields.Char(string="Nota")


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(FleetVehicleOdometer,self).read_group( domain, fields, groupby, offset, limit, orderby, lazy)
        i=0
        for dict_group in res:
            if '__domain' in dict_group:
                group_ids = self.env['fleet.vehicle.odometer'].search(dict_group['__domain'])
                for key,value in dict_group.items():
                    if key == "value":
                        values_list = group_ids.sudo().mapped('value')
                        final = max(values_list) - min(values_list)
                        res[i][key] = final
                    if key == "horometer":
                        horometer_list = group_ids.sudo().mapped('horometer')
                        final = max(horometer_list) - min(horometer_list)
                        res[i][key] = final
                    if key == "truck_horometer":
                        horometer_tr_list = group_ids.sudo().mapped('truck_horometer')
                        final = max(horometer_tr_list) - min(horometer_tr_list)
                        res[i][key] = final
                i+=1
        return res