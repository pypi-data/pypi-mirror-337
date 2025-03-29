# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountInvoiceReportCommercialAddress(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceReportCommercialAddress, cls).setUpClass()

        cls.partner_id = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "street": "Test Street",
                "zip": "1234",
                "city": "Test City",
                "country_id": cls.env.ref("base.us").id,
            }
        )

        cls.partner_id.commercial_partner_id = cls.env["res.partner"].create(
            {
                "name": "Test Commercial Partner",
                "street": "Test Commercial Street",
                "zip": "1234",
                "city": "Test Commercial City",
                "country_id": cls.env.ref("base.us").id,
            }
        )

        cls.move = cls.env["account.move"].create(
            {
                "partner_id": cls.partner_id.id,
            }
        )

    def test_show_commercial_entity_true(self):
        self.move._compute_show_commercial_entity()
        self.assertTrue(
            self.move.show_commercial_entity, "show_commercial_entity should be True"
        )

    def test_show_commercial_entity_false(self):
        self.move.partner_id = self.move.partner_id.commercial_partner_id
        self.move._compute_show_commercial_entity()
        self.assertFalse(
            self.move.show_commercial_entity, "show_commercial_entity should be False"
        )

    def test_show_commercial_entity_default(self):
        self.move.partner_id.commercial_partner_id = self.move.partner_id
        self.move._compute_show_commercial_entity()
        self.assertFalse(
            self.move.show_commercial_entity, "show_commercial_entity should be False"
        )
