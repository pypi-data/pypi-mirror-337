# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    show_commercial_entity = fields.Boolean(
        compute="_compute_show_commercial_entity",
        readonly=False,
        store=True,
    )

    @api.depends("partner_id")
    def _compute_show_commercial_entity(self):
        for move in self:
            move.show_commercial_entity = (
                move.partner_id != move.partner_id.commercial_partner_id
            )
