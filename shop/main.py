import os
from decimal import Decimal

from shop.ingredient import IngredientsStore
from shop.cart import Cart
from shop.discount import BulkDiscount, NoDiscount

if __name__ == '__main__':
    """Challenge text code run"""

    ingredients = [
        ('tomatoes', Decimal('0.15')),
        ('chicken', Decimal('3.49')),
        ('onions', Decimal('2.00')),
        ('rice', Decimal('0.70')),
    ]

    ingredient_store = IngredientsStore(ingredients)

    # or

    csv_filepath = os.path.join('data', 'ingredients.csv')
    ingredient_store = IngredientsStore.init_from_filepath(csv_filepath)

    price = ingredient_store.get_ingredient_price('chicken')

    print("Chinken price:", price)

    tomatoes_nodiscount = NoDiscount('tomatoes')

    buy_one_get_one_free_tomatoes = BulkDiscount('tomatoes', 1, 1)
    buy_two_get_third_free_onions = BulkDiscount('onions', 2, 1)

    discounts = [buy_one_get_one_free_tomatoes, buy_two_get_third_free_onions]

    print("Line total for buy-one-get-one-free-tomatoes situation:",
          buy_one_get_one_free_tomatoes.calculate_line_total())

    shopping_cart = Cart(ingredient_store)

    shopping_cart.add('tomatoes')
    shopping_cart.add('onions', 2)
    shopping_cart.add('rice', 7)

    total_price, total_cart = shopping_cart.get_total()
    total_price_after_discount, total_cart_after_discount = shopping_cart.get_total(discounts)

    print("Total: {:f} Cart: {}".format(total_price, total_cart))
    print("Total: {:f} Cart: {}".format(total_price_after_discount, total_cart_after_discount))
