# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api, exceptions, fields, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    keep_number = fields.Boolean()

    @api.multi
    def button_draft(self):
        # go from canceled state to draft state
        for order in self:
            if order.state != 'cancel':
                raise exceptions.Warning(
                    _("You can't back any order that it's not on cancel "
                      "state. Order: %s" % order.name))
            for invoice in order.invoice_ids:
                invoice.signal_workflow('invoice_cancel')
                invoice.internal_number = False
                invoice.unlink()
            order.order_line.write({'state': 'draft'})
            order.procurement_group_id.unlink()
            for line in order.order_line:
                line.procurement_ids.unlink()
            order.write({'state': 'draft'})
            order.delete_workflow()
            order.create_workflow()
            order.keep_number = True
        return True
