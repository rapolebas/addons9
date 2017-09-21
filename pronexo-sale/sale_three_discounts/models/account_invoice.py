from openerp import fields, models, api
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    discount1 = fields.Float(
        'Discount 1 (%)',
        digits=dp.get_precision('Discount'),
    )
    discount2 = fields.Float(
        'Discount 2 (%)',
        digits=dp.get_precision('Discount'),
    )
    discount3 = fields.Float(
        'Discount 3 (%)',
        digits=dp.get_precision('Discount'),
    )
    discount = fields.Float(
        compute='get_discount',
        inverse='_inverse_discount',
        store=True,
        readonly=True,
    )

    @api.multi
    def _inverse_discount(self):
        for rec in self:
            if rec.invoice_id.type not in ('in_invoice', 'in_refund'):
                _logger.info(
                    'Setting discount should only be used from purchase '
                    'invoices, on sale invoices you should use Discount 1, '
                    '2 and 3.')
                continue
            # we only show discount field on purchase invoices
            rec.discount1 = rec.discount
            rec.discount2 = False
            rec.discount3 = False

    @api.one
    @api.depends('discount1', 'discount2', 'discount3')
    def get_discount(self):
        discount_factor = 1.0
        for discount in [self.discount1, self.discount2, self.discount3]:
            discount_factor = discount_factor * ((100.0 - discount) / 100.0)
        self.discount = 100.0 - (discount_factor * 100.0)
