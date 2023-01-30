from odoo import models, fields, api
import base64
class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = ['l10n_cl.edi.util', 'stock.picking']

    def create_all_delivery_guide(self):
        for record in self:
            record.create_delivery_guide()

"""     def create_delivery_guide(self):
        rec = super(Picking,self).create_delivery_guide()
        report = self.env.ref('10n_cl_edi_stock.action_delivery_guide_report_pdf',False)
        pdf_content, content_type = report._render_qweb_pdf(self.id)
        pdf_name = "Guia de despacho (52) - {} ".format(self.name)
        attachment = self.env['ir.attachment'].create({
            'name': pdf_name,
            'type': 'binary',
            'datas': base64.encodebytes(pdf_content),
            'res_model': self._name,
            'res_id': self.id
        })
        return rec """
