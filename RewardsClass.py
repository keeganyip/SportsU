import math
from datetime import date
import datetime


from dateutil.relativedelta import relativedelta # download 'pip install python-dateutil'


# user hardcode
class user:
    def __init__(self,name,points,id,membertype):
        self.__name = name
        self.__points = points
        self.__point_expiry_date = '23-01-2020'
        self.__id = id
        self.__membertype = membertype

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_points(self):
        return self.__points

    def set_points(self,points):
        self.__points = points


    def get_point_expiry_date(self): # jovan
        return self.__point_expiry_date

    def set_expiry_date(self,new_date): # jovan
        self.__point_expiry_date = new_date

    def get_membertype(self):
        return self.__membertype


u1 = user('zh1',900,1,'P')
u2 = user('zh2',2000,2,'N')


class Reward:
    countReward = 0

    def __init__(self,name,cost,Desc,image,Category):
        self.__name = name
        self.__cost = cost
        self.__Desc = Desc
        self.__image = image
        self.__Category = Category

        Reward.countReward += 1
    def get_name(self):
        return self.__name
    def get_cost(self,user):
        if user == "Staff":
            return self.__cost
        elif user.get_membertype() == "N":
            return self.__cost
        elif user.get_membertype() == "P":
            return math.floor(self.__cost*0.80)
        else:
            return self.__cost
    def get_Desc(self):
        return self.__Desc
    def get_image(self):
        return self.__image

    def get_Category(self):
        return self.__Category

    def set_name(self,name):
        self.__name = name
    def set_cost(self,cost):
        self.__cost = cost
    def set_Desc(self,Desc):
        self.__Desc = Desc

    def set_image(self,image):
        self.__image = image

    def get_modal_id(self):
        modal_id = self.__name
        filtered = modal_id.replace(" ", "")
        filtered = filtered.replace("%","Perc")
        filtered = filtered.replace("$","Do")
        return filtered

    def plus_points(cls,total_amount,user):
        points_to_add = math.floor(total_amount / 10)
        user.set_points(user.get_points() + points_to_add)
        return False



    def extend_points_expiry_date(cls,user):
        new_expiry_date = date.today() + relativedelta(months = 6)
        split_list = str(new_expiry_date).split("-")
        new_expiry_date = (split_list[2]) + "-" + str(split_list[1]) + "-" + str(split_list[0])
        user.set_expiry_date(new_expiry_date)




class RewardsTransaction:
    def __init__(self,date,total_price,id,items):
        self.__total_price = total_price
        self.__id = id
        self.__date = date
        self.__items = items


    def get_date(self):
        return self.__date

    def get_items(self):
        return self.__items

    def get_total_price(self):
        return self.__total_price

    def get_id(self):
        return self.__id


