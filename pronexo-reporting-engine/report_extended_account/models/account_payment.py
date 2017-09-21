# -*- coding: utf-8 -*-
from openerp import models, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def payment_print(self):
        self.ensure_one()
        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.get_report_name(self._name, self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.multi
    def action_payment_sent(self):
        """ Open a window to compose an email, with the edi payment template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(
            'report_extended_account.email_template_edi_receipt', False)
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.payment',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            # mark_invoice_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
