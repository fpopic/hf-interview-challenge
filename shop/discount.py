from abc import abstractmethod, ABCMeta


class AbstractDiscount(metaclass=ABCMeta):
    """
        Abstract interface for discount class
    """

    @abstractmethod
    def calculate_line_total(self):
        """
            Calculates total quantity after discount has been applied
        """
        pass


class NoDiscount(AbstractDiscount):
    """
        No discount is applied and the price remains unaffected.
    """

    def __init__(self, ingredient, quantity=1):
        self.ingredient = ingredient
        self.quantity = quantity

    def calculate_line_total(self):
        return self.quantity


class BulkDiscount(AbstractDiscount):
    """
        A discount that applies when you buy a specific quantity.
        For example, buy one get one free, or, buy two get a third free.
    """

    def __init__(self, ingredient, quantity, free_quantity):
        self.ingredient = ingredient
        self.quantity = quantity
        self.free_quantity = free_quantity

    def calculate_line_total(self):
        return self.quantity + self.free_quantity
