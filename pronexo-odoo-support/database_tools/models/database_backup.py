# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import os
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class database_backup(models.Model):
    _name = 'db.database.backup'
    _description = 'Database Backup'
    _order = "create_date desc"

    database_id = fields.Many2one(
        'db.database',
        string='Database',
        required=True
    )
    date = fields.Datetime(
        string='Date',
        required=True
    )
    keep_till_date = fields.Datetime(
        string='Keep Till date',
        help="Only for manual backups, if not date is configured then backup "
        "won't be deleted.",
    )
    name = fields.Char(
        string='Name',
        required=True
    )
    path = fields.Char(
        string='Path',
        required=True
    )
    full_path = fields.Char(
        string='Path',
        compute='get_full_path',
    )
    type = fields.Selection(
        [('manual', 'Manual'), ('automatic', 'Automatic')],
        string='Type',
        required=True
    )

    @api.one
    @api.depends('path', 'name')
    def get_full_path(self):
        self.full_path = os.path.join(self.path, self.name)

    @api.multi
    def unlink(self):
        for backup in self:
            backup.database_id.remove_directory(backup.full_path)
        return super(database_backup, self).unlink()
