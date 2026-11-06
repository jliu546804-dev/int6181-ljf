"""Unit tests for Problem 3: Order."""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    def test_add_items_and_calculate_regular_order(self):
        self.regular_order.add_item("Book", 20.0, quantity=2, category="general")
        self.regular_order.add_item("Apples", 10.0, quantity=1, category="grocery")
        self.assertEqual(self.regular_order.subtotal, 50.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 3.2)
        self.assertEqual(self.regular_order.shipping_fee, 0.0)
        self.assertEqual(self.regular_order.final_total, 53.2)
        self.assertEqual(self.regular_order.status, "PENDING")
        self.assertEqual(self.regular_order.get_summary()["item_count"], 3)

    def test_gold_tier_and_save10_coupon(self):
        self.gold_order.add_item("Headphones", 100.0, category="electronics")
        self.gold_order.apply_coupon(" save10 ")
        self.assertEqual(self.gold_order.subtotal, 100.0)
        self.assertEqual(self.gold_order.discount_amount, 19.0)
        self.assertEqual(self.gold_order.tax_amount, 6.48)
        self.assertEqual(self.gold_order.shipping_fee, 0.0)
        self.assertEqual(self.gold_order.final_total, 87.48)
        self.assertEqual(self.gold_order.applied_coupon, "SAVE10")

    def test_silver_tier_flat_coupon_and_shipping(self):
        self.silver_order.add_item("Lamp", 40.0, category="general")
        self.silver_order.apply_coupon("FLAT15")
        self.assertEqual(self.silver_order.subtotal, 40.0)
        self.assertEqual(self.silver_order.discount_amount, 17.0)
        self.assertEqual(self.silver_order.tax_amount, 1.84)
        self.assertEqual(self.silver_order.shipping_fee, 5.99)
        self.assertEqual(self.silver_order.final_total, 30.83)

    def test_remove_item_recalculates_order(self):
        self.regular_order.add_item("Pen", 5.0, quantity=2)
        self.regular_order.add_item("Bag", 20.0)
        self.regular_order.remove_item("Pen", quantity=1)
        self.assertEqual(self.regular_order.items["Pen"]["quantity"], 1)
        self.assertEqual(self.regular_order.subtotal, 25.0)
        self.assertEqual(self.regular_order.tax_amount, 2.0)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.final_total, 32.99)

    def test_checkout_cancel_and_invalid_operations(self):
        with self.assertRaises(ValueError):
            self.regular_order.checkout()
        self.regular_order.add_item("Notebook", 10.0)
        self.assertTrue(self.regular_order.checkout())
        self.assertEqual(self.regular_order.status, "PAID")
        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Pencil", 1.0)
        with self.assertRaises(RuntimeError):
            self.regular_order.cancel()
        with self.assertRaises(ValueError):
            Order("BAD", customer_tier="platinum")
        with self.assertRaises(ValueError):
            Order("ORD400").apply_coupon("UNKNOWN")


if __name__ == "__main__":
    unittest.main()
