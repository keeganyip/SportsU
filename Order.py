class Order:
    orderID = 0

    def __init__(self, product):
        Order.orderID += 1
        self.__id = Order.orderID
        self.__product = product
        self.__supplier = ""
        self.__quantity = ""
        self.__date = ""
        self.__time = ""
        self.__status = ""

    def get_id(self):
        return self.__id

    def get_product(self):
        return self.__product

    def get_supplier(self):
        return self.__supplier

    def get_quantity(self):
        return int(self.__quantity)

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_status(self):
        return self.__status

    def set_id(self, id):
        self.__id = id

    def set_product(self, product):
        self.__product = product

    def set_supplier(self, supplier):
        self.__supplier = supplier

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_date(self, date):
        self.__date = date

    def set_time(self, time):
        self.__time = time

    def set_status(self, status):
        self.__status = status

    def id_to_product(self, id):
        if id == self.__id:
            return self.__product
