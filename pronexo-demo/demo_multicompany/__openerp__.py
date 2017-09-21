# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Demo of Multicompany Environment',
    'version': '9.0.1.0.0',
    'category': 'Tools',
    'sequence': 14,
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'board',
        'l10n_ar_account_reports',
        'website_portal_followup',
        'account_reports_followup',
        'account_accountant',
        'l10n_ar_afipws_fe',
        'account_multicompany_usability',
        'account_multic_fix',
        'account_debt_management',
        'account_move_helper',
        'account_no_translation',
        'base_currency_inverse_rate',
        'account_clean_cancelled_invoice_number',
        'account_invoice_change_currency',
        'account_invoice_commercial',
        'account_invoice_company_search',
        'account_invoice_journal_group',
        # 'account_invoice_operation',
        # este se auto instala solo si estaba account usability, lo forzamos
        # por las dudas
        'adhoc_account_planner',
        'account_usability',
        'account_statement_move_import',
        'account_invoice_prices_update',
        'account_invoice_tax_wizard',
        'l10n_ar_aeroo_einvoice',
        'l10n_ar_aeroo_purchase',
        'l10n_ar_aeroo_sale',
        'l10n_ar_aeroo_stock',
        'l10n_ar_aeroo_payment_group',
        'l10n_ar_currency_update',
        'l10n_ar_padron_afip',
        'l10n_ar_bank',
        'product_catalog_aeroo_report_public_categ',
        'product_no_translation',
        'product_price_currency',
        'product_pricelist',
        'product_price_taxes_included',
        'product_replenishment_cost_rule',
        'product_sale_price_by_margin',
        'product_template_search_by_barcode',
        'product_website_categ_search',
        'purchase_quotation_products',
        'sale_quotation_products',
        'purchase_discount',
        'stock_inventory_preparation_filter',
        'base_state_active',
        'project_description',
        'project_duplicate_fix',
        'project_kanban_open_project',
        # 'sale_order_type_user_default',
        'sale_procurement_date_confirm',
        'hr_attendance',
        'base_technical_features',
        'account_transfer_unreconcile',
        'l10n_ar_account_vat_ledger',

        'hr_appraisal',
        'account_financial_report_qweb',
        'account_tax_balance',
        # odoo enterprise modules
        'account_contract_dashboard',
        'hr_holidays_gantt',
        'mass_mailing_themes',
        'website_contract',
        'website_form_editor',
        'account_payment_fix',
        'purchase_contract',

        'web_support_client_issue',

        'l10n_ar_aeroo_base',
        'l10n_ar_aeroo_einvoice',
        'l10n_ar_aeroo_invoice',
        'l10n_ar_aeroo_purchase',
        'l10n_ar_aeroo_sale',
        'l10n_ar_aeroo_stock',
        'project_issue_solutions',
        'stock_picking_labels',
        'stock_picking_list',
        'hr_recruitment',
        'hr_expense',
        'database_cleanup',
        'google_account',
        'google_calendar',
        'google_drive',
        'google_spreadsheet',
        'hr_contract',
        # 'hr_timesheet_invoice', DEPRECIADO
        # 'knowledge', DEPRECIADO
        # 'l10n_ar_base_vat', DEPRECIADO
        'l10n_ar_padron_afip',
        'mail_tracking',
        'mass_editing',
        'payment_todopago',
        'project_issue_sheet',
        'stock_usability',
        # 'support_branding', DEPRECIADO PARA ENTEPRISE
        # 'warning_box', DEPRECIADO
        # 'web_advanced_search_wildcard', NO MIGRADO
        # 'web_advanced_search_x2x', NO MIGRADO
        # 'web_clean_navbar', DEPRECIADO
        'web_export_view',
        # 'web_ir_actions_act_window_message', DEPRECIADO
        # 'web_kanban_sparkline', DEPRECIADO
        # 'web_recipients_uncheck', NO MIGRADO
        # 'web_search_with_and', NO MIGRADO
        'web_sheet_full_width',
        # 'web_shortcuts', DEPRECIADO
        'website_partner',
        'web_widget_many2many_tags_multi_selection',
        'account_reconciliation_menu',
        'adhoc_modules',
        'project_category',
        'sale_prices_update',
        'mis_builder',
        'product_search_supplier_code',
        'project_closure_restrictions',
        'sale_contract_restrict_domain',
        'product_supplier_search',
        'hr_holidays',
        'auth_signup_verify_email',
        'purchase_multic_fix',
        'web_easy_switch_company',
        'website_blog',
        'website_crm',
        'website_twitter',
        'marketing',
        'project_issue_fix',
    ],
    'data': [
        'config_data.xml',
        'users_data.xml',
        # last load lang (so user is already created)
        'load_es_lang.yml',
        'account_data.yml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
