# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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
    "name": "Reindex documents",
    "version": "8.0.1.0.0",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Knowledge Management",
    "summary": "Reindex your already uploaded documents",
    "depends": [
        'document',
    ],
    "data": [
        "views/knowledge_config_settings.xml",
        "views/ir_attachment.xml",
    ],
    "post_init_hook": 'post_init_hook',
    "auto_install": False,
    'installable': False,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
