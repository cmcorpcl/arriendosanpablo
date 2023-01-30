# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Agrega campo auth_sii'

    company_rut_sii = fields.Char(string="RUT SII")
    company_sii_pass = fields.Char(string="Clave SII")