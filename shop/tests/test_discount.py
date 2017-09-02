from unittest import TestCase
from shop.discount import NoDiscount, BulkDiscount


class TestBulkDiscount(TestCase):
    def test_calculate_line_total(self):
        discount = NoDiscount("test_ingredient_1", 5)

        acutal_line_total = discount.calculate_line_total()
        expected_line_total = 5

        self.assertEqual(acutal_line_total, expected_line_total)


class TestNoDiscount(TestCase):
    def test_calculate_line_total(self):
        discount = BulkDiscount("test_ingredient_1", 5, 2)

        acutal_line_total = discount.calculate_line_total()
        expected_line_total = 5 + 2

        self.assertEqual(acutal_line_total, expected_line_total)
