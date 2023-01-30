from odoo import models, fields, api
from odoo.osv import expression

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    is_in_maintance = fields.Boolean(string="¿Está en mantenimiento?")

    def name_get(self):
        res = []
        for lot in self:
            name = lot.name
            if (lot.ref):
                name = "[" + lot.ref  + "] " + name
            res.append((lot.id, name))
        return res

    @api.model
    def name_search(self,name,args=None, operator='Ilike', limit=100,name_get_uid=None):
        if args is None:
            args=[]
        domain= args + ['|', ('name',operator,name), ('ref',operator,name)]
        return super(StockProductionLot,self).search(domain, limit=limit).name_get()
