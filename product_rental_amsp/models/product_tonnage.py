from odoo import models, fields, api



class ProductTonnage(models.Model):
    _name = 'product.tonnage'

    name = fields.Char(string="Nombre")
    product_ids = fields.Many2many('product.product','product_tonnage_rel','tonnage_id','product_id', string="Productos")
