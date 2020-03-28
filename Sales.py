class Sales:
    countID = 0

    def __init__(self, date):
        Sales.countID += 1
        self.__salesID = Sales.countID
        self.__date = date
        self.__purchases = []
        self.__refund_status = ' '
        self.__refund_reason = 'None'

    def get_sales_date(self):
        return self.__date

    def get_purchases(self):
        return self.__purchases

    def get_refund_status(self):
        return self.__refund_status

    def get_refund_reason(self):
        return self.__refund_reason

    def get_salesID(self):
        return self.__salesID

    def set_sales_date(self, date):
        self.__date = date

    def set_purchases(self, purchases):
        self.__purchases = purchases

    def set_refund_status(self, status):
        self.__refund_status = status

    def set_refund_reason(self, reason):
        self.__refund_reason = reason

    def sales_total(self):
        total = 0
        for i in self.__purchases:
            total += int(i.get_quantity()) * int(i.get_ListPrice())
        return total

    def __iter__(self):
        yield self.__purchases