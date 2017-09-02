import csv
from decimal import Decimal
from fastnumbers import isfloat
import logging


class IngredientsStore:
    """
        A wrapper class for dictionary: <Ingredient, Price>
    """

    def __init__(self, ingredients):
        self.ingredients = dict(ingredients)

    @classmethod
    def init_from_filepath(cls, csv_filepath):
        """
            CSV file header: "ingredient","price"

            CSV file example:

                "ingredient","price"
                "tomatoes",0.15
                "apples",2.20
                ...
                "bananas",3.00

           Invalid lines will be omitted.
        """
        try:
            with open(csv_filepath) as file:
                reader = csv.reader(file)
                ingredients = dict()
                for line in reader:
                    # ingredient, price
                    if len(line) == 2:
                        ingredient, price = line[0], line[1]
                        if len(ingredient) and isfloat(price):
                            if Decimal(price) >= 0.00:
                                ingredients[ingredient] = Decimal(price)
                            else:
                                logging.warning("Price can't be negative!", line)
                    else:
                        logging.warning("Invalid line:", line)
                return IngredientsStore(ingredients)
        except IOError:
            logging.warning("File doesn't exist!")

    def get_ingredient_price(self, ingredient):
        """Returns a price for an ingredient"""
        if ingredient in self.ingredients:
            return self.ingredients[ingredient]
        else:
            return None
