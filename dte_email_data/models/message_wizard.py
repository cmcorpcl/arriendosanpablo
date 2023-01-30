# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MessageWizard(models.TransientModel):
    _name = 'dte_email_data.message.wizard'
    _description = 'Mensaje de pedidos'

    message = fields.Text(string="Usuarios no encontrados: ", readonly=True)
    message_no_rut = fields.Text(string="Usuarios sin RUT: ", readonly=True)

    def redirect_to_list(self):
        return  {
                'name': 'Contactos',
                'view_mode':'tree,kanban,form,map,activity',
                'view_type':'form',
                'res_model':'res.partner',
                        'views': [(self.env.ref('base.view_partner_tree').id, 'tree'),
                        (self.env.ref('base.res_partner_kanban_view').id, 'kanban'),
                        (self.env.ref('base.view_partner_form').id, 'form'),
                        (self.env.ref('contacts_enterprise.res_partner_view_map').id, 'map'),
                        (self.env.ref('mail.res_partner_view_activity').id, 'activity')],
                'type':'ir.actions.act_window',
                'target': 'main',
                'nodestroy': True
        }

    def redirect_to_list_dte_partner(self):
        return  {
                'name': 'Listado de contribuyentes SII',
                'view_mode':'tree',
                'view_type':'form',
                'res_model':'dte_email_data.dte_partner',
                'views': [(self.env.ref('dte_email_data.dte_partner_tree').id, 'tree'),],
                'type':'ir.actions.act_window',
                'target': 'main',
                'nodestroy': True
        }
