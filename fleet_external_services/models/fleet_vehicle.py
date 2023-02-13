from odoo import models, fields, api

class FleetVehicle(models.Model):
    _inherit = ['fleet.vehicle']

    state_mantention_km = fields.Char(string="Est. Mantención km")
    state_mantention_tr = fields.Char(string="Est. Mantención camión")
    state_mantention_hr = fields.Char(string="Est. Mantención hr")
    compute_mantention = fields.Char(string="Compute Mantención", compute="_compute_mantention")
    number_serie_id = fields.Many2one('stock.production.lot',string="Numero de serie")

    def _compute_mantention(self):
        for record in self:
            record.compute_mantention = "No compute"
            record.state_mantention_km = ""
            record.state_mantention_hr = ""
            record.state_mantention_tr = ""
            if record.model_id:
                km_ids = record.model_id.km_ids
                truck_horometer_ids = record.model_id.truck_horometer_ids
                crane_horometer_ids = record.model_id.crane_horometer_ids
                services_odometer_cr = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',record.id),('state','not in',['todo','cancelled']),('odo_hor','=','odo')])
                services_horometer_tr = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',record.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor_tr')])
                services_horometer = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',record.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor')])
                odometer = self.env['fleet.vehicle.odometer'].search([('vehicle_id','=',record.id)], order='date desc', limit=1)
                horometer = self.env['fleet.vehicle.odometer'].search([('vehicle_id','=',record.id)], order='date desc', limit=1)
                pass_services_cr = False
                pass_services_tr = False
                pass_services_hr = False
                max_service_value = 0
                max_service_horometer_tr = 0
                max_service_horometer = 0
                for service in services_horometer:
                    if max_service_horometer < service.horometer_note:
                        max_service_horometer  = service.horometer_note
                if  odometer.horometer > max_service_horometer:
                    pass_services_hr = True
                for service in services_horometer_tr:
                    if max_service_horometer_tr < service.horometer_note:
                        max_service_horometer_tr  = service.horometer_note
                for service in services_odometer_cr:
                    if max_service_value < service.odometer_note:
                        max_service_value  = service.odometer_note
                if odometer.value > max_service_value:
                    pass_services_cr = True
                if odometer.truck_horometer > max_service_value:
                    pass_services_tr = True
                if pass_services_cr:
                    for km in km_ids:
                         if odometer.value >= km.km and km.km > max_service_value:
                            record.compute_mantention = "Compute"
                            record.state_mantention_km = "Odómetro "+ str(km.km)+ ' km'
                if pass_services_tr:
                    for horometer in truck_horometer_ids:
                         if odometer.value >= horometer.horometer and horometer.horometer > max_service_horometer_tr:
                            record.compute_mantention = "Compute"
                            record.state_mantention_tr = "Horómetro Camión "+ str(horometer.horometer)+ ' hrs'
                if pass_services_hr:
                    for horometer in crane_horometer_ids:
                        if odometer.horometer >= horometer.horometer and horometer.horometer > max_service_horometer:
                            record.compute_mantention = "Compute"
                            record.state_mantention_hr = "Horómetro Grúa " + str(horometer.horometer) + ' hrs'

    @api.onchange('number_serie_id')
    def _onchange_number_serie_id(self):
        for record in self:
            if record.number_serie_id:
                record.license_plate = record.number_serie_id.name
