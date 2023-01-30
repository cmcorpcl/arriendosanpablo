from odoo import models, fields, api

class MailChannel(models.Model):
    _name = 'mail.channel'
    _inherit = ['mail.channel']

    notification_fleet = fields.Boolean(string="Notificación Mantenimiento")
