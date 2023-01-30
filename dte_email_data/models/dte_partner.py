# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DtePartner(models.Model):
    _name = 'dte_email_data.dte_partner'
    _description = 'Contribuyentes obtenidos de SII'

    rut = fields.Char(string='RUT', required=False )
    bussiness_line = fields.Char(string="Razón social")
    resolution_number = fields.Char(string="Numero de resolución")
    resolution_date = fields.Char(string="Fecha de resolución")
    dte_email = fields.Char(string='Correo DTE')
    url = fields.Char(string='URL')
