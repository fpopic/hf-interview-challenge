from unittest import TestCase

from decimal import Decimal

from shop.ingredient import IngredientsStore


class TestIngredientsStore(TestCase):
    def test_init_from_filepath_with_some_invalid_lines(self):
        store = IngredientsStore.init_from_filepath('data/test_ingredients.csv')

        actual_ingredients = store.ingredients
        expected_ingredients = dict([('apples', Decimal('7.00'))])

        self.assertDictEqual(actual_ingredients, expected_ingredients)
