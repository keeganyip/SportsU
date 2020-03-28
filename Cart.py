class Cart:
    countID = 0

    def __init__(self):
        Cart.countID += 1
        self.__cartID = Cart.countID
        self.__quantity = 0
        self.__name = ""
        self.cost = 0


    def get_name(self):
        return self.__name

    def get_cost(self):
        return self.__cost

    def get_quantity(self):
        return self.__quantity

    def get_cartID(self):
        return self.__cartID

    def set_name(self, name):
        self.__name = name

    def set_cost(self, cost):
        self.__cost = cost

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def total_cost(self):
        total = self.__cost * self.__quantity
        return total



