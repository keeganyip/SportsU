from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, FileField,\
    BooleanField, DateField, DecimalField, FloatField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired


class CreateUserForm(Form):

    firstName = StringField('First Name',
                            [validators.Length(min=1,max=150), validators.DataRequired()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.DataRequired()])

    gender = RadioField('Gender',[validators.DataRequired()],
                         choices=[('F', 'Female'), ('M', 'Male')],
                         default='F')
    email = StringField("Email Address",[validators.Length(min=5,max=50), validators.DataRequired()])

    password = StringField('Password:',[validators.Length(min=5,max=50), validators.DataRequired()],widget=PasswordInput(hide_value=False))
    passwordRepeat = StringField('Confirm password:', [validators.Length(min=5,max=50), validators.DataRequired()],widget=PasswordInput(hide_value=False))

    accounttype = SelectField('Type',[validators.Optional()],choices=[('Admin','Admin'),('Staff','Staff'),('User','User')],default='User')
    phone = StringField("Phone Number: ", validators=[validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message= 'Phone number needs to start with 6,8 or 9'),validators.Length(min=8, max=8), DataRequired()])
    city = SelectField('City:',choices=[('Singapore','Singapore')])
    address = StringField('Address:',[validators.data_required()])
    unit = StringField('Unit number:',[validators.data_required()])

    postal = IntegerField('Postal code:',validators=[validators.data_required(message='Please Enter Integers only')])


class UpdateForm(Form):

    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])

    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')


class changepassword(Form):

    newpassword = StringField('New password:', [validators.Length(min=5, max=50), validators.data_required()],
                                 widget=PasswordInput(hide_value=False))
    passwordRepeat = StringField('Confirm New password:', [validators.Length(min=5, max=50), validators.data_required()],
                                 widget=PasswordInput(hide_value=False))

class userchangeinfo(Form):
    firstName = StringField('First Name',
                            [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.DataRequired()])

    gender = RadioField('Gender', [validators.DataRequired()],
                        choices=[('F', 'Female'), ('M', 'Male')],
                        default='F')
    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])
    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')
    phone = StringField("Phone Number: ", validators=[
        validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message='Phone number needs to start with 6,8 or 9'),
        validators.Length(min=8, max=8), DataRequired()])
    city = SelectField('City:', choices=[('Singapore', 'Singapore')])
    address = StringField('Address:', [validators.data_required()])
    unit = StringField('Unit number:', [validators.data_required()])

    postal = IntegerField('Postal code:',[validators.data_required(message='Please Enter Integers only')])

class Userchangeinfo(Form):
    firstName = StringField('First Name',
                            [validators.Length(min=1, max=150), validators.Optional()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.Optional()])

    gender = RadioField('Gender', [validators.Optional()],
                        choices=[('F', 'Female'), ('M', 'Male')],
                        default='F')
    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])
    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')
    phone = StringField("Phone Number: ")
    city = SelectField('City:', choices=[('Singapore', 'Singapore')],default='Singapore')
    address = StringField('Address:', [validators.Optional()])
    unit = StringField('Unit number:', [validators.Optional()])

    postal = IntegerField('Postal code:',[validators.Optional()])

class checkoutuserchangeinfo(Form):
    firstName = StringField('First Name',
                            [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name',
                           [validators.Length(min=1, max=150), validators.DataRequired()])

    email = StringField("Email Address", [validators.Length(min=5, max=50), validators.DataRequired()])
    accounttype = SelectField('Type', [validators.Optional()],
                              choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('User', 'User')], default='User')
    phone = StringField("Phone Number: ", validators=[
        validators.Regexp(r'^(?:\+?65)?[689]\d{7}$', message='Phone number needs to start with 6,8 or 9'),
        validators.Length(min=8, max=8), DataRequired()])
    city = SelectField('City:', choices=[('Singapore', 'Singapore')])
    address = StringField('Address:', [validators.data_required()])
    unit = StringField('Unit number:', [validators.data_required()])

    postal = IntegerField('Postal code:',[validators.data_required(message='Please Enter Integers only')])


class userchangepassword(Form):
    oldpassword = StringField('Old Password:', [validators.Length(min=5, max=50), validators.data_required()],
                           widget=PasswordInput(hide_value=False))
    newpassword = StringField('New password:', [validators.Length(min=5, max=50), validators.data_required()],
                                 widget=PasswordInput(hide_value=False))
    passwordRepeat = StringField('Confirm New password:', [validators.Length(min=5, max=50), validators.data_required()],
                                 widget=PasswordInput(hide_value=False))


class CreateProductForm(Form):
    style = {'class': 'form-control'}
    Name = StringField("Product Name:", [validators.DataRequired()], render_kw=style)

    Brand = SelectField('Brand:', [validators.DataRequired()],
                        choices=[('', 'Select'), ('Nike', 'Nike'),('Adidas','Adidas'),('UnderArmour','Under Armour')],
                        render_kw=style)

    Category = SelectField('Category:', [validators.DataRequired()],
                           choices=[('', 'Select'), ('Shoes', 'Shoes')],
                           render_kw=style)

    RetailPrice = IntegerField('Retail Price:', [validators.DataRequired(message='Please Enter Integers only')], render_kw=style)

    Quantity = IntegerField("Quantity:", [validators.DataRequired(message='Please Enter Integers only')], render_kw=style)

    ListPrice = IntegerField('List Price:',[validators.DataRequired(message='Please Enter Integers only')],render_kw=style)

    Sale = BooleanField("Sale:",[validators.Optional()])

    SalePrice = IntegerField("Sale Price:",[validators.Optional()],render_kw=style)

    SaleStartDate = DateField('Sale Start Date:',[validators.Optional()],render_kw=style)

    SaleEndDate = DateField('Sale End Date:',[validators.Optional()],render_kw=style)

    Member = BooleanField("Membership:",[validators.Optional()])


class RewardsForm(Form):
    Reward_Name = StringField('Name:',[validators.Length(min=1,max=150), validators.DataRequired()],render_kw={"placeholder":"Enter Reward Name..."})
    Reward_Cost = IntegerField('Points Required:',[validators.DataRequired(message='Please Enter Integers only')],render_kw={"placeholder":"Enter Number of Points Required..."})
    Reward_Desc = TextAreaField('Description:',[validators.DataRequired()],render_kw={"placeholder":"Enter Brief Description..."})
    Reward_Category = SelectField('Select Category:',[validators.DataRequired()], choices=[('FnB', 'Food and Beverage'), ('Shopping', 'Shopping'), ("Entertainment", "Entertainment"),("Travel","Travel")] )


class quantityForm(Form):
    quantity = SelectField('', [validators.DataRequired()], choices=[(1, 1), (2, 2), (3, 3),(4,4),(5,5)])


class CreateShoppingCart(Form):
    productName = StringField('Product Name',
                            [validators.Length(min=1,max=150),
                             validators.DataRequired()])

    quantity = StringField('Quantity',
                            [validators.Length(min=1,max=150),
                             validators.DataRequired()])


class Refund(Form):
    refund_reason = TextAreaField('Reason for Refund', [validators.DataRequired()])

    refund_status = SelectField('Status', [validators.Optional()], choices=[('', 'Select'), ('Approved', 'Approved'),
                                ('Rejected', 'Rejected'), ('Pending', 'Pending')], default='')

class CreditCard(Form):
    card_type = SelectField('', [validators.DataRequired()], choices=[('Visa', 'Visa'), ('Master', 'Master')], default='')

    card_number = StringField(" Credit Card Number *: ", validators=[validators.Regexp(r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14})$', message='Invalid Card Number'),
                                                                     validators.Length(min=3, max=200, message=''), DataRequired()])

    card_expiry_month = SelectField('', [validators.DataRequired()], choices=[('01', '01'), ('02', '02'),
                                                                                    ('03', '03'), ('04', '04'),
                                                                                    ('05', '05'), ('06', '06'),
                                                                                    ('07', '07'), ('08', '08'),
                                                                                    ('09', '09'), ('10', '10'),
                                                                                    ('11', '11'), ('12', '12')], default='05')

    card_expiry_year = SelectField('', [validators.DataRequired()], choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022')], default='2022')

    card_cvv = IntegerField('Card CVV', [validators.DataRequired(message='Please enter 3 Digits'), validators.number_range(min=100, max=999, message="Invalid CVV")], widget=PasswordInput(hide_value=False))

class UpdateCart(Form):
    updateqty = IntegerField([validators.DataRequired()])

class AddSupplierForm(Form):
    style = {'class': 'form-control'}

    supplierName = StringField('Company Name:', [validators.Length(min=1,max=150),validators.DataRequired()], render_kw=style)

    supplierAddress = StringField('Address (Postal Code):', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw=style)

    website = StringField('Website:', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw=style)

    phone = IntegerField("Contact Number:", [validators.DataRequired()], render_kw=style)

    contact = StringField("Who to Contact:", [validators.DataRequired()], render_kw=style)

    product = SelectField("Product:", [validators.DataRequired()], choices=[], default="", render_kw=style)

    price = IntegerField("Cost Price:", [validators.DataRequired()], render_kw=style)


class AddOrder(Form):
    style = {'class': 'form-control'}

    quantity = IntegerField("Quantity:", [validators.DataRequired()], render_kw=style)


class OrderStatus(Form):
    status = SelectField("Status:", choices=[('P', 'Pending'), ('D', 'Delivered')], default='P')
