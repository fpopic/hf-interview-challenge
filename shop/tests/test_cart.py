from unittest import TestCase
from shop.cart import Cart
from shop.discount import BulkDiscount, NoDiscount
from shop.ingredient import IngredientsStore
from decimal import Decimal


class TestCart(TestCase):
    def test_add_not_available_ingredient(self):
        store = IngredientsStore([('test_ingredient_1', Decimal('1.00'))])
        cart = Cart(store)
        cart.add('test_ingredient_2')

        expected_cart_size = Decimal('1.00')
        actual_cart_size = len(cart.ingredient_store.ingredients)

        self.assertEqual(expected_cart_size, actual_cart_size)

    def test_get_total_after_no_discount(self):
        ingredients = [
            ('test_ingredient_1', Decimal('2.00')),
            ('test_ingredient_2', Decimal('3.00'))
        ]
        store = IngredientsStore(ingredients)

        cart = Cart(store)
        cart.add('test_ingredient_1', 1)
        cart.add('test_ingredient_2', 7)

        discounts = [
            NoDiscount('test_ingredient_2')
        ]

        actual_total_price, actual_total_cart = cart.get_total(discounts)

        expected_total_price = Decimal(23.00)
        expected_total_cart = [('test_ingredient_1', 1), ('test_ingredient_2', 7)]

        self.assertEqual(actual_total_price, expected_total_price)
        self.assertCountEqual(actual_total_cart, expected_total_cart)

    def test_get_total_after_bulk_discount(self):
        ingredients = [
            ('test_ingredient_1', Decimal('2.00')),
            ('test_ingredient_2', Decimal('3.00'))
        ]
        store = IngredientsStore(ingredients)

        cart = Cart(store)
        cart.add('test_ingredient_1', 1)
        cart.add('test_ingredient_2', 7)

        discounts = [
            BulkDiscount('test_ingredient_2', 7, 1)
        ]

        actual_total_price, actual_total_cart = cart.get_total(discounts)

        expected_total_price = Decimal(23.00)
        expected_total_cart = [('test_ingredient_1', 1), ('test_ingredient_2', 7 + 1)]

        self.assertEqual(actual_total_price, expected_total_price)
        self.assertCountEqual(actual_total_cart, expected_total_cart)
