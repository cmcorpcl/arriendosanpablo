from odoo import models, fields, api
from datetime import datetime

class FleetVehicleFuel(models.Model):
    _name = 'fleet.vehicle.fuel'
    _order = 'date desc'

    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehiculo")
    driver_id = fields.Many2one('res.partner',string="Responsable de carga")
    date = fields.Datetime(string="Fecha", default=datetime.today())
    time = fields.Float(string="Tiempo")
    horometer = fields.Float(string="Horometro Grúa")
    horometer_tr = fields.Float(string="Horometro Camión")
    start_fuel = fields.Float(string="Odómetro al cargar")
    end_fuel = fields.Float(string="Litros Cargados")
    note = fields.Char(string="Nota")
    rental_id = fields.Many2one('sale.order',string="Arriendo asociado", domain="[('is_rental_order','=',True)]")


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(FleetVehicleFuel,self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)
        i=0
        for dict_group in res:
            if '__domain' in dict_group:
                group_ids = self.env['fleet.vehicle.fuel'].search(dict_group['__domain'])
                for key,value in dict_group.items():
                    if key == "start_fuel":
                        values_list = group_ids.sudo().mapped('start_fuel')
                        final = max(values_list) - min(values_list)
                        res[i][key] = final
                i+=1
        return res