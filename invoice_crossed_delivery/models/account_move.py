from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    picking_ref_ids = fields.One2many('stock.picking','invoice_union_id', string="Guias de despacho", domain="[('id', 'in', allowed_picking_ids)]")
    allowed_picking_ids = fields.One2many('stock.picking', compute='_compute_allowed_picking_ids')

    def write(self,vals):
        ids_reference = self.l10n_cl_reference_ids.ids
        ids_picking = self.picking_ref_ids.ids
        ids_picking_result = []
        ids_picking_delete = []
        ids_picking_add = []
        one_picking = False
        if 'picking_ref_ids' in vals:
            print(vals['picking_ref_ids'])
            for key in vals['picking_ref_ids']:
                if key[0] == 6:
                    ids_picking_result = key[2]
                    one_picking = "Muchos"
                elif key[0] == 3:
                    ids_picking_delete.append(key[1])
                    one_picking = "Solo Uno"
        if one_picking == "Solo Uno":
            to_delete_ref = self.l10n_cl_reference_ids.search([('delivery_guide_id',"in", ids_picking_delete)])
            for ref in to_delete_ref:
                if 'l10n_cl_reference_ids' in vals:
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
                else:
                    vals['l10n_cl_reference_ids'] = []
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
        elif one_picking == "Muchos" :
            ids_picking_delete = list(set(ids_picking) - set(ids_picking_result))
            ids_picking_add = list(set(ids_picking_result) - set(ids_picking))
            to_delete_ref = self.l10n_cl_reference_ids.search([('delivery_guide_id',"in", ids_picking_delete)])
            to_add_ref = self.env['stock.picking'].search([('id','in',ids_picking_add)])
            for ref in to_delete_ref:
                if 'l10n_cl_reference_ids' in vals:
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
                else:
                    vals['l10n_cl_reference_ids'] = []
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
            for picking in to_add_ref:
                val_ref = {
                    "delivery_guide_id": picking.id,
                    "origin_doc_number": str(picking.l10n_latam_document_number),
                    "l10n_cl_reference_doc_type_selection": picking.l10n_latam_document_type_id.code,
                    "date": picking.date_done
                }
                if 'l10n_cl_reference_ids' in vals:
                    vals['l10n_cl_reference_ids'].append([0,0,val_ref])
                else:
                    vals['l10n_cl_reference_ids'] = []
                    vals['l10n_cl_reference_ids'].append([0,0,val_ref])
        print(vals)
        res = super(AccountMove,self).write(vals)
        return res

    @api.depends('invoice_line_ids')
    def _compute_allowed_picking_ids(self):
        for record in self:
            all_ids= []
            ids = []
            if record.invoice_line_ids:
                for line in record.invoice_line_ids:
                    for sale in line.sale_line_ids:
                        all_ids.append(sale.order_id.id)
                        [ids.append(x) for x in all_ids if x not in ids]
            delivery_guides = self.env['stock.picking'].search([ '&', '|', ('invoice_union_id','=',record.id),('invoice_union_id','=',False),('l10n_latam_document_number','!=',False),('sale_id','in',ids),('state','=','done')])
            record.allowed_picking_ids = delivery_guides

    def button_cancel(self):
        for record in self:
            ids_picking_delete = record.picking_ref_ids.ids
            to_delete_ref = record.l10n_cl_reference_ids.search([('delivery_guide_id',"in", ids_picking_delete)])
            vals={}
            for ref in to_delete_ref:
                if 'l10n_cl_reference_ids' in vals:
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
                else:
                    vals['l10n_cl_reference_ids'] = []
                    vals['l10n_cl_reference_ids'].append([2,ref.id])
            vals['picking_ref_ids'] = []
            vals['picking_ref_ids'].append([5,0,0])
            record.write(vals)
        return super(AccountMove, self).button_cancel()