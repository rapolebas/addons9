# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields, _
from openerp.exceptions import UserError
from openerp.tools.float_utils import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_status = fields.Selection([
        ('no', 'Nothing to Deliver'),
        ('to deliver', 'To Deliver'),
        ('delivered', 'Delivered'),
    ],
        string='Delivery Status',
        compute='_get_delivered',
        store=True,
        readonly=True,
        default='no'
    )

    @api.multi
    def action_cancel(self):
        for order in self:
            for pick in order.picking_ids:
                if pick.state == 'done':
                    raise UserError(_(
                        'Unable to cancel sale order %s as some receptions'
                        ' have already been done.') % (order.name))
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(_(
                        "Unable to cancel this sale order. You must first "
                        "cancel related bills and pickings."))
        return super(SaleOrder, self).action_cancel()

    # dejamos el depends a qty_delivered por mas que usamos all_qty_delivered
    # total son iguales pero qty_delivered es storeado
    @api.depends(
        'state', 'order_line.qty_delivered', 'order_line.product_uom_qty')
    def _get_delivered(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for order in self:
            if order.state not in ('sale', 'done'):
                order.delivery_status = 'no'
                continue

            if any(float_compare(
                    line.all_qty_delivered, line.product_uom_qty,
                    precision_digits=precision) == -1
                    for line in order.order_line):
                order.delivery_status = 'to deliver'
            elif all(float_compare(
                    line.all_qty_delivered, line.product_uom_qty,
                    precision_digits=precision) >= 0
                    for line in order.order_line):
                order.delivery_status = 'delivered'
            else:
                order.delivery_status = 'no'

    @api.multi
    def button_reopen(self):
        self.write({'state': 'sale'})
