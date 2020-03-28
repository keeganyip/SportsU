import datetime
from datetime import date


class Product:
    countID = 0

    def __init__(self,name,brand,category,price,quantity,image):
        Product.countID += 1
        self.__productID = Product.countID
        self.__name = name
        self.__brand = brand
        self.__category = category
        self.__retailprice = price
        self.__quantity = quantity
        self.__image = image
        self.__listPrice = price
        self.__status = "Active"
        self.__memberonly = False
        self.__sale = False
        self.__salePrice = 0
        self.__saleStartDate = datetime.datetime(1, 1, 1)
        self.__saleEndDate = datetime.datetime(1, 1, 1)

    def get_productID(self):
        return self.__productID

    def get_productName(self):
        return self.__name

    def get_productBrand(self):
        return self.__brand


    def get_category(self):
        return self.__category

    def get_retailprice(self):
        return self.__retailprice

    def get_quantity(self):
        return self.__quantity

    def get_image(self):
        return self.__image

    def get_ListPrice(self):
        return self.__listPrice

    def get_status(self):
        return self.__status

    def get_sale_price(self):
        return self.__salePrice

    def get_sale_Start_date(self):
        return self.__saleStartDate

    def get_sale_End_date(self):
        return self.__saleEndDate

    def get_sale_status(self):
        return self.__sale

    def get_memberOnly(self):
        return self.__memberonly

    def set_productID(self,ID):
        self.__productID = ID

    def set_name(self,name):
        self.__name = name

    def set_brand(self,brand):
        self.__brand = brand

    def set_category(self,category):
        self.__category = category

    def set_retailprice(self,price):
        self.__retailprice = price

    def set_quantity(self,quantity):
        self.__quantity = quantity

    def set_image(self,image):
        self.__image = image

    def set_ListPrice(self,ListPrice):
        self.__listPrice = ListPrice

    def set_status(self,status):
        self.__status = status

    def set_sale_price(self,sale_price):
        self.__salePrice = sale_price

    def set_sale_start_date(self,sale_Startdate):
        self.__saleStartDate = sale_Startdate

    def set_sale_end_date(self,sale_Enddate):
        self.__saleEndDate = sale_Enddate

    def set_sale_status(self,sale_status):
        self.__sale = sale_status

    def set_memberOnly(self,memberOnly):
        self.__memberonly = memberOnly

    def sale(self,amount):
        current = self.get_quantity()
        self.set_quantity(current-amount)

    def add_stock(self,stock):
        current = self.get_quantity()
        self.set_quantity(current+stock)

    def totalprice(self):
        price = self.get_ListPrice()
        if self.get_sale_status():
            if self.get_sale_Start_date() <= date.today() <= self.get_sale_End_date():
                price = self.get_sale_price()
        return price


    def __str__(self):
        return "ID:{},Name:{},Brand:{},Category:{},Price:{},Quantity:{}".format(self.get_productID(),
                                                                                            self.get_productName(),
                                                                                            self.get_productBrand(),
                                                                                            self.get_category(),
                                                                                            self.get_retailprice(),
                                                                                            self.get_quantity())

x = Product('x','x','x','x','x,','x')
