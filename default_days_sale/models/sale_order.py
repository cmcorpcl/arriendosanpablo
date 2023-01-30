from datetime import timedelta
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    commitment_date = fields.Datetime('Delivery Date', copy=False,
                                    states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                                    default=lambda self: fields.Datetime.now() + timedelta(days=int(self.env.company.days_to_sum)) if self.env.company.days_plus_default else False,
                                    help="This is the delivery date promised to the customer. "
                                        "If set, the delivery order will be scheduled based on "
                                        "this date rather than product lead times.")