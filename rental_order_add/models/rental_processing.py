from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RentalProcessingLine(models.TransientModel):
    _inherit = ['rental.order.wizard.line']


    def _apply(self):
        """Apply the wizard modifications to the SaleOrderLine.

        :return: message to log on the Sales Order.
        :rtype: str
        """
        print('Hola lineas')
        msg = self._generate_log_message()
        for wizard_line in self:
            order_line = wizard_line.order_line_id
            print('Hola por dentro 1')
            if wizard_line.status == 'pickup' and wizard_line.qty_delivered > 0:
                print('Hola por dentro 2')
                order_line.sudo().update({
                    'product_uom_qty': max(order_line.product_uom_qty, order_line.qty_delivered + wizard_line.qty_delivered),
                    'qty_delivered': order_line.qty_delivered + wizard_line.qty_delivered
                })
                print('Hola por dentro 3.0')
                if order_line.pickup_date > fields.Datetime.now():
                    print('Hola por dentro 3.1')
                    order_line.pickup_date = fields.Datetime.now()

            elif wizard_line.status == 'return' and wizard_line.qty_returned > 0:
                print('Hola por dentro 4')
                if wizard_line.is_late:
                    print('Hola por dentro 5')
                    # Delays facturation
                    order_line._generate_delay_line(wizard_line.qty_returned)
                print('Hola por dentro 6')
                order_line.update({
                    'qty_returned': order_line.qty_returned + wizard_line.qty_returned
                })
        print('Hola por dentro 7')
        return msg
