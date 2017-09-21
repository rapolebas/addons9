# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class ProductCatalogReport(models.Model):
    _inherit = 'product.product_catalog_report'

    category_type = fields.Selection(
        [('public_category', 'Public Category'),
         ('accounting_category', 'Accounting Category')],
        'Category Type',
        required=True,
        default='accounting_category',
    )
    public_category_ids = fields.Many2many(
        'product.public.category',
        'product_catalog_report_categories_public',
        'product_catalog_report_id',
        'category_id',
        'Product Categories Public',
    )

    # TODO remove this
    # @api.one
    # @api.onchange('category_type')
    # def change_category_type(self):
    #     if (
    #             self.category_type == 'public_category' and
    #             not self.categories_order
    #             ):
    #         self.categories_order = 'parent_left, sequence, name'

    @api.multi
    def prepare_report(self):
        self = super(ProductCatalogReport, self).prepare_report()
        if self.category_type == 'public_category':
            categories = self.public_category_ids
            if self.include_sub_categories and categories:
                categories = self.env['product.public.category'].search(
                    [('id', 'child_of', categories.ids)])
        else:
            categories = self.category_ids
            if self.include_sub_categories and categories:
                categories = self.env['product.category'].search(
                    [('id', 'child_of', categories.ids)])

        return self.with_context(
            category_ids=categories.ids,
            category_type=self.category_type)
