class Supplier:
    supplierID = 0

    def __init__(self, name, address, website, phone, contact, product, price):
        Supplier.supplierID += 1
        self.__id = Supplier.supplierID
        self.__supplier_name = name
        self.__address = address
        self.__website = website
        self.__phone = phone
        self.__contact = contact
        self.__brand = ""
        self.__product = product
        self.__price = price
        self.__validity = ""

    def get_id(self):
        return self.__id

    def get_supplier_name(self):
        return self.__supplier_name

    def get_supplier_address(self):
        return self.__address

    def get_website(self):
        return self.__website

    def get_phone(self):
        return self.__phone

    def get_contact(self):
        return self.__contact

    def get_brand(self):
        return self.__brand

    def get_product(self):
        return self.__product

    def get_price(self):
        return self.__price

    def get_validity(self):
        return self.__validity

    def set_id(self, id):
        self.__id = id

    def set_supplier_name(self, name):
        self.__supplier_name = name

    def set_supplier_address(self, address):
        self.__address = address

    def set_website(self, website):
        self.__website = website

    def set_phone(self, phone):
        self.__phone = phone

    def set_contact(self, contact):
        self.__contact = contact

    def set_brand(self, brand):
        self.__brand = brand

    def set_product(self, product):
        self.__product = product

    def set_price(self, price):
        self.__price = price

    def set_validity(self, validity):
        self.__validity = validity
