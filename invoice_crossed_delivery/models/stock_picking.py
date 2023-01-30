from odoo import models, fields, api

class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    has_invoice = fields.Boolean(string="¿Tiene factura relacionada?")
    invoice_union_id = fields.Many2one('account.move', string="Factura relacionada")

    def name_get(self):
        res = []
        for picking in self:
            name = picking.name
            if picking.l10n_latam_document_number:
                name = "[GD" + str(picking.l10n_latam_document_number)  + "] " + name
            res.append((picking.id, name))
        return res

    @api.model
    def name_search(self,name,args=None, operator='Ilike', limit=100,name_get_uid=None):
        if args is None:
            args=[]
        domain= args + ['|', ('name',operator,name), ('l10n_latam_document_number',operator,name)]
        return super(StockPicking,self).search(domain, limit=limit).name_get()
