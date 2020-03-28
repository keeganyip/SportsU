import shelve

class User:
    countID = 0

    def __init__(self, firstName, lastName, gender, password,email,phone,city,address,unit,postal,date):
        User.countID += 1
        self.__userID = User.countID
        self.__firstName = firstName
        self.__lastName = lastName
        self.__gender = gender
        self.__membership = 'M'
        self.__membertier = ''
        self.__password = password
        self.__email = email
        self.__accounttype = 'User'
        self.__date = date
        self.__phone = phone
        self.__city = city
        self.__address = address
        self.__unit = unit
        self.__postal = postal
        #ZH
        self.__points = 0
        self.__point_expiry_date = ''
        self.__membertype = 'N'

    def get_name(self):
        return self.__firstName + ' ' + self.__lastName

    def get_userID(self):
        return self.__userID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_membertier(self):
        return self.__membertier

    def get_remarks(self):
        return self.__remarks

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_accounttype(self):
        return self.__accounttype

    def get_date(self):
        return self.__date

    def get_phone(self):
        return self.__phone

    def get_city(self):
        return self.__city

    def get_address(self):
        return self.__address

    def get_unit(self):
        return self.__unit

    def get_postal(self):
        return self.__postal

    def set_phone(self,phone):
        self.__phone = phone

    def set_userID(self,userID):
        self.__userID = userID

    def set_firstName(self,firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_membership(self, membership):
        self.__membership = membership

    def set_membertier(self,membertier):
        self.__membertier = membertier

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_gender(self,gender):
        self.__gender = gender

    def set_password(self,password):
        self.__password = password

    def set_email(self,email):
        self.__email = email

    def set_accounttype(self,accounttype):
        self.__accounttype = accounttype

    def set_date(self,date):
        self.__date = date

    def set_city(self, city):
        self.__city = city

    def set_address(self, address):
        self.__address = address

    def set_unit(self, unit):
        self.__unit = unit

    def set_postal(self, postal):
        self.__postal = postal

    #ZH
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

    def set_membertype(self,type):
        self.__membertype = type

a1 = User("Admin","asd","Male",'password',"admin@admin.com",'96230219','Singapore','address','08-799',123456,'2019-12-30')
a1.set_accounttype("Admin")
u1 = User('Andrea','Tan','Male','password','andreatan@thebest.com','92345678','Singapore','address','08-799',133456,'2019-12-30')
u1.set_expiry_date('20-03-2020')
u1.set_points(999)
u2 = User('zh','ho','Male','password','newuser@email.com','92345638','Singapore','address','09-799',133456,'2019-12-30')
u3 = User('zhh','hoo','Male','password','existinguser@email.com','92345238','Singapore','address','09-799',133456,'2020-01-30')
u3.set_points(1200)
u3.set_expiry_date('20-03-2020')
usersDict = {}
db = shelve.open('user.db','c')
usersDict[a1.get_userID()] = a1
usersDict[u1.get_userID()] = u1
usersDict[u2.get_userID()] = u2
usersDict[u3.get_userID()] = u3
db['Users'] = usersDict
print(usersDict)
