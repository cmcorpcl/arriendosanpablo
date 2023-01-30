# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class DestinationZone(models.Model):
    _name = "destination.zone"
    _rec_name = "name"

    name = fields.Char(string="Nombre de zona",required=True)