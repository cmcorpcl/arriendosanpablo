from odoo import models, fields, api

class Product(models.Model):
    _inherit = 'product.template'

    tonnage_ids = fields.Many2many('product.tonnage','product_tonnage_rel','product_id','tonnage_id',string="Tonelajes")
    template_quotation = fields.Many2one('ir.ui.view',string="Template",domain=[('type','=','qweb'),('product_template_amsp','=',True)])
