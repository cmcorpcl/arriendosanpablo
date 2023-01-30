from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_connect_id = fields.Many2one('purchase.order', string='Asociar pedido de compra', domain="[('invoice_status','=', 'to invoice'),('partner_id', '=', partner_id)]")
    compute_all_purchase_connect = fields.Char(string="Pedidos de compras asociados", compute="_compute_all_purchase")


    def write(self, vals):
        if 'purchase_connect_id' in vals:
            vals['purchase_id'] = vals['purchase_connect_id']
            purchase_order = self.env['purchase.order'].search([('id', '=', vals['purchase_connect_id'])],limit=1)
            #if len(purchase_order) > 0:
                #vals['purchase_id'] = vals['purchase_connect_id']
        res = super(AccountMove, self).write(vals)
        return res

    @api.onchange('purchase_connect_id')
    def _change_real(self):
        self.purchase_id = self.purchase_connect_id
        super(AccountMove,self)._onchange_purchase_auto_complete()
        self.purchase_connect_id = False

    @api.depends('invoice_line_ids')
    def _compute_all_purchase(self):
        for record in self:
            string=""
            purchase_list = []
            counter=0
            for line in record.invoice_line_ids:
                if line.purchase_order_id:
                    if line.purchase_order_id.name not in purchase_list:
                        purchase_list.append(line.purchase_order_id.name)
            if len(purchase_list) > 0:
                purchase_list.sort()
                for name in purchase_list:
                    if counter ==0:
                        string += name
                    else:
                        string += ', ' + name
                    counter += 1
            record.compute_all_purchase_connect = string