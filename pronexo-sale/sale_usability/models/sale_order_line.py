# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields, _
from openerp.exceptions import UserError
from openerp.tools.float_utils import float_compare
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # add context so show sale data by default
    order_id = fields.Many2one(
        context={'show_sale': True}
    )
    # agregamoe este campo para facilitar compatibilidad con
    # sale_usability_return_invoicing
    all_qty_delivered = fields.Float(
        string='All Delivered',
        compute='_compute_all_qty_delivered',
        help='Todo lo entregado sin descontar las devoluciones',
        digits=dp.get_precision('Product Unit of Measure'),
    )

    @api.multi
    @api.depends('qty_delivered')
    def _compute_all_qty_delivered(self):
        for rec in self:
            rec.all_qty_delivered = rec.qty_delivered

    delivery_status = fields.Selection([
        ('no', 'Not purchased'),
        ('to deliver', 'To Deliver'),
        ('delivered', 'Delivered'),
    ],
        string='Delivery Status',
        compute='_compute_delivery_status',
        store=True,
        readonly=True,
        copy=False,
        default='no'
    )

    @api.depends('order_id.state', 'qty_delivered', 'product_uom_qty')
    def _compute_delivery_status(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self:
            if line.state not in ('sale', 'done'):
                line.delivery_status = 'no'
                continue

            if float_compare(
                    line.all_qty_delivered, line.product_uom_qty,
                    # line.qty_delivered, line.product_uom_qty,
                    precision_digits=precision) == -1:
                line.delivery_status = 'to deliver'
            elif float_compare(
                    line.all_qty_delivered, line.product_uom_qty,
                    # line.qty_delivered, line.product_uom_qty,
                    precision_digits=precision) >= 0:
                line.delivery_status = 'delivered'
            else:
                line.delivery_status = 'no'

    @api.multi
    def button_cancel_remaining(self):
        for rec in self:
            old_product_uom_qty = rec.product_uom_qty
            if rec.qty_invoiced > rec.qty_delivered:
                raise UserError(_(
                    'You can not cancel remianing qty to deliver because '
                    'there are more product invoiced than the delivered. '
                    'You should correct invoice or ask for a refund'))
            rec.product_uom_qty = rec.qty_delivered
            # to_cancel_procurements = rec.procurement_ids.filtered(
            #     lambda x: x.state != 'done')
            to_cancel_moves = rec.mapped(
                'procurement_ids.move_ids').filtered(
                lambda x: x.state != 'done')
            to_cancel_moves.action_cancel()
            # to_cancel_procurements.cancel()
            # because cancel dont update operations, we re asign
            # to_cancel_procurements.mapped('move_ids.picking_id').filtered(
            to_cancel_moves.mapped('picking_id').filtered(
                lambda x: x.state not in ['draft', 'cancel']).action_assign()
            rec.order_id.message_post(
                body=_(
                    'Cancel remaining call for line "%s" (id %s), line '
                    'qty updated from %s to %s') % (
                        rec.name, rec.id,
                        old_product_uom_qty, rec.product_uom_qty))
