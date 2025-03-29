# Copyright 2025 Angel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestPricelistItemBrand(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.brand_1 = cls.env["product.brand"].create({"name": "Brand X"})
        cls.brand_2 = cls.env["product.brand"].create({"name": "Brand Y"})

        cls.product_1 = cls.env["product.template"].create(
            {"name": "Product 1", "product_brand_id": cls.brand_1.id}
        )

        cls.product_2 = cls.env["product.template"].create(
            {"name": "Product 2", "product_brand_id": cls.brand_2.id}
        )

        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist Test",
            }
        )

        cls.pricelist_item = cls.env["product.pricelist.item"].create(
            {
                "product_brand_ids": [(6, 0, [cls.brand_1.id])],
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_1.id,
                "pricelist_id": cls.pricelist.id,
            }
        )

    def test_is_applicable_for_product_with_brand(self):
        is_applicable_product_1 = self.pricelist_item._is_applicable_for(
            self.product_1, 1
        )
        self.assertTrue(
            is_applicable_product_1, "Pricelist applicable to Product 1 with Brand X."
        )

    def test_is_applicable_for_product_without_brand(self):
        is_applicable_product_2 = self.pricelist_item._is_applicable_for(
            self.product_2, 1
        )
        self.assertFalse(
            is_applicable_product_2,
            "Pricelist not applicable to Product 2 with Brand Y.",
        )

    def test_is_applicable_for_product_without_brand_or_no_brand(self):
        product_without_brand = self.env["product.template"].create(
            {
                "name": "Product without brand",
            }
        )
        is_applicable_product = self.pricelist_item._is_applicable_for(
            product_without_brand, 1
        )
        self.assertFalse(
            is_applicable_product, "Pricelist not applicable to Product without brand"
        )
