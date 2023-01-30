# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_digital_signature(self, user_id=None):
        """
        This method looks for a digital signature that could be used to sign invoices for the current company.
        If the digital signature is intended to be used exclusively by a single user, it will have that user_id
        otherwise, if the user is false, it is understood that the owner of the signature (which is always
        a natural person) shares it with the rest of the users for that company.
        """
        if user_id is not None:
            user_certificates = self.sudo().l10n_cl_certificate_ids.filtered(
                lambda x: x._is_valid_certificate() and x.user_id.id == user_id and
                          x.company_id.id == self.id and not x.only_dte)
            if user_certificates:
                return user_certificates[0]
        shared_certificates = self.sudo().l10n_cl_certificate_ids.filtered(
            lambda x: x._is_valid_certificate() and not x.user_id and x.company_id.id == self.id and not x.only_dte)
        if not shared_certificates:
            raise UserError(_('There is not a valid certificate for the company: %s') % self.name)

        return shared_certificates[0]