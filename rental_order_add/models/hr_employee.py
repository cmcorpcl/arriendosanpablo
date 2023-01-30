from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployeeBase(models.AbstractModel):
    _inherit = ['hr.employee.base']

    autorized_credit = fields.Boolean(string='¿Puede autorizar credito?')