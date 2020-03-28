class Inventory:
    stockID = 0

    def __init__(self, name, supplier, quantity):
        Inventory.stockID += 1
        self.__product_id = Inventory.stockID
        self.__product_name = name
        self.__supplier = supplier
        self.quantity = quantity

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__product_name

    def get_supplier(self):
        return self.__supplier

    def set_id(self, id):
        self.__product_id = id

    def set_name(self, name):
        self.__product_name = name

    def set_supplier(self, supplier):
        self.__supplier = supplier
