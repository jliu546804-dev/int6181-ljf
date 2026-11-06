"""
Unit tests for Problem 3: Order

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the Order object
(e.g., subtotal, discount_amount, tax_amount, shipping_fee, final_total, status)
to verify state consistency under various conditions.

Running tests:
    python -m unittest test_problem3.py -v
"""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    
    def test_regular_order_calculates_multiple_attributes(self):
        """Test subtotal, tax, shipping and total for a regular order."""
        self.regular_order.add_item("Book", 20.0, quantity=2)

        self.assertEqual(self.regular_order.subtotal, 40.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 3.2)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.final_total, 49.19)
        self.assertEqual(self.regular_order.status, "PENDING")

    def test_gold_order_with_save10_coupon(self):
        """Test gold membership and SAVE10 coupon together."""
        self.gold_order.add_item("Laptop", 100.0)
        self.gold_order.apply_coupon("SAVE10")

        self.assertEqual(self.gold_order.subtotal, 100.0)
        self.assertEqual(self.gold_order.discount_amount, 19.0)
        self.assertEqual(self.gold_order.tax_amount, 6.48)
        self.assertEqual(self.gold_order.shipping_fee, 0.0)
        self.assertEqual(self.gold_order.final_total, 87.48)
        self.assertEqual(self.gold_order.applied_coupon, "SAVE10")

    def test_silver_order_with_flat15_coupon(self):
        """Test silver membership and FLAT15 coupon."""
        self.silver_order.add_item("Monitor", 60.0)
        self.silver_order.apply_coupon("FLAT15")

        self.assertEqual(self.silver_order.subtotal, 60.0)
        self.assertEqual(self.silver_order.discount_amount, 18.0)
        self.assertEqual(self.silver_order.tax_amount, 3.36)
        self.assertEqual(self.silver_order.shipping_fee, 5.99)
        self.assertEqual(self.silver_order.final_total, 51.35)
        self.assertEqual(self.silver_order.applied_coupon, "FLAT15")

    def test_remove_item_recalculates_order(self):
        """Test that removing an item updates order amounts."""
        self.regular_order.add_item("Apple", 10.0, quantity=3, category="grocery")
        self.regular_order.add_item("Book", 20.0)
        self.regular_order.remove_item("Book")

        self.assertEqual(self.regular_order.subtotal, 30.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertEqual(self.regular_order.tax_amount, 0.0)
        self.assertEqual(self.regular_order.shipping_fee, 5.99)
        self.assertEqual(self.regular_order.final_total, 35.99)
        self.assertNotIn("Book", self.regular_order.items)

    def test_checkout_updates_order_status(self):
        """Test checkout and prevent further changes to a paid order."""
        self.regular_order.add_item("Book", 20.0)
        result = self.regular_order.checkout()

        self.assertTrue(result)
        self.assertEqual(self.regular_order.status, "PAID")
        self.assertEqual(self.regular_order.subtotal, 20.0)
        self.assertEqual(self.regular_order.final_total, 27.59)
        self.assertEqual(len(self.regular_order.items), 1)

        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Pen", 2.0)





if __name__ == "__main__":
    unittest.main()
