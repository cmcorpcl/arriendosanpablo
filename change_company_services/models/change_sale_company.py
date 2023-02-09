from odoo import models, fields, api

class ChangeSaleCompany(models.TransientModel):
    _name = 'change.sale.company'
    _description = "Cambio de compañia para ventas y alquileres que esten confirmadas"

    company_id = fields.Many2one('res.company',string="Compañia")
    sale_order_id = fields.Many2one('sale.order',string="Pedido de venta")

    def action_change(self):
        for record in self:
            if record.sale_order_id and record.company_id:
                warehouse_id = self.env['ir.default'].sudo().get_model_defaults('sale.order').get('warehouse_id')
                record.sale_order_id.sudo().write({'company_id': record.company_id.id,'warehouse_id': warehouse_id or record.sale_order_id.user_id.with_company(self.company_id.id)._get_default_warehouse_id().id})
                for line in record.sale_order_id.order_line:
                    line.sudo().write({'company_id':record.company_id})
                    if line.task_id:
                        project_id = False
                        project_company = self.env['project.project'].sudo().search([('id','in',line.task_id.project_id.companie_related_project_ids.ids),('company_id','=',record.company_id.id)],limit=1)
                        if project_company:
                            print('encontro!')
                            project_id = project_company.id
                        line.task_id.sudo().write({'company_id':record.company_id.id,'sale_line_id':line.id,'project_id':project_id})
