# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, tools, api, _
from openerp.exceptions import ValidationError
import random
import string
import os


class database_type(models.Model):

    _name = 'infrastructure.database_type'
    _description = 'database_type'
    _order = 'sequence'

    sequence = fields.Integer(
        'Sequence',
        default=10,
    )
    name = fields.Char(
        string='Name',
        required=True
    )
    description = fields.Text(
        string='Description',
    )
    is_production = fields.Boolean(
        help='Databases of this type are used to get data to invoice on '
        'contracts and also used to get priority when duplicating'
    )
    backups_enable = fields.Boolean(
        'Backups Enable?',
    )
    check_database = fields.Boolean(
        'Check Databse with cron',
        help="Suggest Check Databases Automatically. Suggested for instances "
        "that restart automatically"
    )
    demo_data = fields.Boolean(
        string='Demo Data?',
        help='Use demo data by default on databases?'
    )
    prefix = fields.Char(
        string='Prefix',
        required=True,
        size=8
    )
    max_dbs_per_contract = fields.Integer(
        string='Max. Dbs per contract',
        # TODO we should use contracts instead of environment
        # TODO we should use max dbs instead of instance
        help='Maximum instances of this type that can exist per environment',
    )
    odoo_run_prefix = fields.Char(
        string='Odoo Run Prefix',
        help='For eg. used for resources limitation'
    )
    postgres_run_prefix = fields.Char(
        string='Postgres Run Prefix',
        help='For eg. used for resources limitation'
    )
    url_prefix = fields.Char(
        string='URL Prefix'
    )
    service_type = fields.Selection([
        ('docker', 'Docker Restart'),
        # ('upstart', 'Upstart Service'),
        ('no_service', 'No Service')],
        default='docker',
        required=True,
    )
    type = fields.Selection(
        [('normal', 'Normal'),
         ('protected', 'Protected'),
         ('auto_deactivation', 'Auto Deactivation'),
         ('auto_drop', 'Auto Drop'),
         ('auto_deact_and_drop', 'Auto Deactivation and Drop')],
        'Type',
        help="Depending on the type:"
        "* Normal: nothing special is made"
        "* Protected: needs special confirmation before some operations"
        "* Auto Deactivation: automatically deactivated on deactivation date"
        "* Auto Drop: automatically dropped on deactivation date"
        "* Auto Deactivation and Drop: automatically deactivated on"
        "deactivation date and automatically dropped on deactivation date",
        required=True,
        default='normal'
    )
    sources_type = fields.Selection([
        ('own', 'Own'), ('clone_from', 'Clone From'), ('use_from', 'Use From')
    ],
        'Sources Type',
        required=True,
        default='own',
        help='* own: sources are cloned from host (git, bitbucet, etc)\n'
        '* clone_from: sources are cloned from another instance'
        '* use_from: sources are used from another instance'
    )
    sources_from_id = fields.Many2one(
        'infrastructure.database_type',
        string='Sources From',
    )
    color = fields.Integer(
        string='Color'
    )
    auto_drop_days = fields.Integer(
        string='Automatic Drop Days'
    )
    protect_db = fields.Boolean(
        string='Protect Databases?'
    )
    auto_deactivation_days = fields.Integer(
        string='Automatic Deactivation Days'
    )
    install_lang_id = fields.Selection(
        tools.scan_languages(),
        string='Install Language',
    )
    db_filter = fields.Many2one(
        'infrastructure.db_filter',
        string='DB Filter',
        help='It will be used as default on Instances',
    )
    workers = fields.Selection(
        [('clasic_rule', 'Clasic Rule'), ('fix_number', 'Fix Number')],
        string='Workers Filter',
        required=True,
        default='clasic_rule',
        help='Clasic Rule means workers = server_processors * 2 + 1'
    )
    workers_number = fields.Integer(
        'Workers Number',
    )
    server_mode_value = fields.Char(
        'Server Mode Value',
    )
    instance_log_level = fields.Selection([
        (u'info', 'info'), (u'debug_rpc', 'debug_rpc'),
        (u'warn', 'warn'), (u'test', 'test'), (u'critical', 'critical'),
        (u'debug_sql', 'debug_sql'), (u'error', 'error'), (u'debug', 'debug'),
        (u'debug_rpc_answer', 'debug_rpc_answer')],
        string='Default Instance Log Level',
        default='info',
        required=True,
    )

    @api.onchange('service_type')
    def change_service_type(self):
        if self.service_type != 'no_service':
            self.check_database = True
        else:
            self.check_database = False

    @api.multi
    def get_password(self):
        self.ensure_one()
        # TODO depreciar db_admin_pass e instance_admin_pass que ya no los
        # usamos
        chars = string.ascii_letters + string.digits
        # no usamos estas porque nos dan error con docker
        # + '!@#$%^&*()'
        random.seed = (os.urandom(1024))
        return ''.join(random.choice(chars) for i in range(20))
