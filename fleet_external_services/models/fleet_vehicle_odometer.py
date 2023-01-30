from odoo import _,models, fields, api
from datetime import datetime

class FleetVehicleOdometer(models.Model):
    _name = 'fleet.vehicle.odometer'
    _inherit = ['fleet.vehicle.odometer']

    truck_horometer = fields.Float(string="Horómetro Camión")
    horometer = fields.Float(string="Horómetro Grúa")
    time = fields.Float(string="Tiempo")

    @api.model
    def create(self,values):
        res = super(FleetVehicleOdometer, self).create(values)
        vehicle_id = self.env['fleet.vehicle'].search([('id','=',values['vehicle_id'])],limit=1)
        partner_id = self.env['res.partner'].search([('category_id.is_bot_mantention','=','True')],limit=1)
        if 'value' in values:
            km_ids = vehicle_id.model_id.km_ids
            type_km = 'Camión'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','odo')])
            self.notification_km_mantention(values['value'],vehicle_id,partner_id,services,km_ids,type_km)
        if 'truck_horometer' in values:
            truck_horometer_ids = vehicle_id.model_id.truck_horometer_ids
            type_km = 'Camión'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor_tr')])
            self.notification_hrs_mantention(values['truck_horometer'],vehicle_id,partner_id,services,truck_horometer_ids,type_km)
        if 'horometer' in values:
            crane_horometer_ids = vehicle_id.model_id.crane_horometer_ids
            type_km = 'Grúa'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor')])
            self.notification_hrs_mantention(values['horometer'],vehicle_id,partner_id,services,crane_horometer_ids,type_km)
        return res


    def write(self,values):
        res = super(FleetVehicleOdometer, self).write(values)
        vehicle_id = self.vehicle_id
        if 'vehicle_id' in values:
            vehicle_id = self.env['fleet.vehicle'].search([('id','=',values['vehicle_id'])],limit=1)
        partner_id = self.env['res.partner'].search([('category_id.is_bot_mantention','=','True')],limit=1)
        if 'value' in values:
            km_ids = vehicle_id.model_id.km_ids
            type_km = 'Camión'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','odo')])
            self.notification_km_mantention(values['value'],vehicle_id,partner_id,services,km_ids,type_km)
        if 'truck_horometer' in values:
            truck_horometer_ids = vehicle_id.model_id.truck_horometer_ids
            type_km = 'Camión'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor_tr')])
            self.notification_km_mantention(values['truck_horometer'],vehicle_id,partner_id,services,truck_horometer_ids,type_km)
        if 'horometer' in values:
            crane_horometer_ids = vehicle_id.model_id.crane_horometer_ids
            type_km = 'Grúa'
            services = self.env['fleet.vehicle.log.services'].search([('vehicle_id','=',vehicle_id.id),('state','not in',['todo','cancelled']),('odo_hor','=','hor')])
            self.notification_hrs_mantention(values['horometer'],vehicle_id,partner_id,services,crane_horometer_ids,type_km)
        return res


    def notification_km_mantention(self,value,vehicle_id,partner_id,services,km_ids,type_km):
        pass_services = False
        max_service_value = 0
        for service in services:
            if max_service_value < service.odometer_note:
                max_service_value  = service.odometer_note
        if value > max_service_value:
            pass_services = True
        if pass_services:
            for km in km_ids:
                if value >= km.km and km.km > max_service_value and km.counter_mantention < 2:
                    km.counter_mantention = km.counter_mantention + 1
                    tags_string = ""
                    for tag in km.tags_ids:
                        tags_string = tags_string + tag.name + ', \n'
                    message = "Aviso N°" + str(km.counter_mantention)+ ": Se requiere hacer mantención por odómetro de "+ type_km +" a la maquina de modelo "+ vehicle_id.model_id.name +' de matricula ' +  vehicle_id.license_plate +' ya que sobrepaso los '+ str(km.km) +' km, se sugiere: \n' + tags_string
                    created_message =  self.env['mail.message'].sudo().create({
                            'email_from': partner_id.email, # add the sender email
                            'author_id': partner_id.id, # add the creator id
                            'model': 'mail.channel', # model should be mail.channel
                            'message_type': 'comment', # model should be mail.channel
                            'subtype_id': self.env.ref('mail.mt_comment').id,
                            'body': message , # here add the message body
                            'channel_ids': [(6,0, self.env['mail.channel'].search([('notification_fleet','=','True')]).ids)], # This is the channel where you want to send the message and all the users of this channel will receive message # here add the channel you created.
                        })
                    create_notification = self.env['fleet.service.notification'].sudo().create({
                        'date': datetime.now(),
                        'number': km.counter_mantention,
                        'vehicle_id': vehicle_id.id,
                        'notification': 'Mantención Odómetro '+type_km + ' ' + str(km.km)+'km \n' + tags_string,
                    })

    def notification_hrs_mantention(self,horometer,vehicle_id,partner_id,services,crane_horometer_ids,type_km):
        pass_services = False
        max_service_horometer = 0
        for service in services:
            if max_service_horometer < service.horometer_note:
                max_service_horometer  = service.horometer_note
        if horometer > max_service_horometer:
            pass_services = True
        if pass_services:
            for horometer_id in crane_horometer_ids:
                if horometer >= horometer_id.horometer and horometer_id.horometer > max_service_horometer and horometer_id.counter_mantention < 2:
                    horometer_id.counter_mantention = horometer_id.counter_mantention + 1
                    tags_string = ""
                    for tag in horometer_id.tags_ids:
                        tags_string = tags_string + tag.name + ', \n'
                    message = "Aviso N°" + str(horometer_id.counter_mantention)+ ": Se requiere hacer mantención por horómetro de "+ type_km + " a la maquina de modelo "+ vehicle_id.model_id.name +' de matricula ' +  vehicle_id.license_plate +' ya que sobrepaso las '+ str(horometer_id.horometer) +' hrs, se sugiere: \n' + tags_string
                    created_message = self.env['mail.message'].sudo().create({
                            'email_from': partner_id.email, # add the sender email
                            'author_id': partner_id.id, # add the creator id
                            'model': 'mail.channel', # model should be mail.channel
                            'message_type': 'comment', # model should be mail.channel
                            'subtype_id': self.env.ref('mail.mt_comment').id,
                            'body': message , # here add the message body
                            'channel_ids': [(6,0, self.env['mail.channel'].search([('notification_fleet','=','True')]).ids)], # This is the channel where you want to send the message and all the users of this channel will receive message # here add the channel you created.
                        })
                    create_notification = self.env['fleet.service.notification'].sudo().create({
                        'date': datetime.now(),
                        'number': horometer_id.counter_mantention,
                        'vehicle_id': vehicle_id.id,
                        'notification': 'Mantención Horómetro ' +type_km + ' '+str(horometer_id.horometer)+'hrs \n' + tags_string,
                    })
