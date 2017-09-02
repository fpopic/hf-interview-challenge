from decimal import Decimal

from shop.discount import BulkDiscount, NoDiscount
import logging


class Cart:
    def __init__(self, ingredient_store):
        # a wrapper of <Ingredient, Price>
        self.ingredient_store = ingredient_store
        # dictionary <Ingredient, Quantity>
        self.shopping_cart = dict()


    def add(self, ingredient, quantity=1):
        """
            Adds an ingredient in a cart. If an ingredient is already present in a cart,
            the quantity will increase for a given quantity.
        """
        if ingredient in self.ingredient_store.ingredients:
            self.shopping_cart[ingredient] = self.shopping_cart.get(ingredient, 0) + quantity
        else:
            logging.warning(
                "%s can't be added to cart, because it isn't available in the ingredient store." % ingredient
            )

    def get_total(self, discounts=None):
        """
            This method optionally takes a list of Discount objects that
            are applied to items in the cart when calculating the total.

            Method has no sideeffects on cart or ingredient store.
            Returns total price, total cart
        """

        total_price = Decimal(0.00)
        total_cart = []

        # create constant time dictionary from discount list
        # <<ingredient, quantity>, discount>
        discounts_dict = dict()
        if discounts is not None:
            discounts_dict = dict([((discount.ingredient, discount.quantity), discount) for discount in discounts])

        for ingredient, quantity in self.shopping_cart.items():

            price = self.ingredient_store.get_ingredient_price(ingredient)
            total_price += price * quantity

            #  apply quantity discounts
            if (ingredient, quantity) in discounts_dict:
                discount = discounts_dict[(ingredient, quantity)]

                # BulkDiscount can be applied
                if type(discount) is BulkDiscount:
                    if discount.quantity == quantity:
                        total_cart.append((ingredient, discount.calculate_line_total()))
                    else:
                        total_cart.append((ingredient, quantity))

                # NoDiscount can be applied
                elif type(discount) is NoDiscount:
                    total_cart.append((ingredient, discount.calculate_line_total()))

            # regular quantity
            else:
                total_cart.append((ingredient, quantity))

        return total_price, total_cart
