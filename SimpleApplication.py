import Product
import User, RewardsClass, Cart, Sales, SalesProduct, Supplier, Order
import shelve
from datetime import datetime, date

from RewardsClass import RewardsTransaction  # ZH
import os  # upload file

from flask import Flask, render_template, request, redirect, url_for, flash, session, Markup

from Forms import CreateUserForm, UpdateForm, changepassword, userchangepassword, userchangeinfo, CreateProductForm, \
    RewardsForm, quantityForm, Refund, UpdateCart, AddSupplierForm, AddOrder, OrderStatus, CreditCard, LoginForm
from RewardsClass import u1, u2
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Keegan'
app.config['MYSQL_PASSWORD'] = '96259519'
app.config['MYSQL_DB'] = 'sportsu'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['RECAPTCHA_PUBLIC_KEY'] ='6LcSEagZAAAAAOR9ygpzgvdgMphdRW-uj7mkVjf2'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcSEagZAAAAACKWVPGBDwM32cnkfACvH3o8Zdsm'
app.config["IMAGE_UPLOADS"] = "static\img\RewardsPicUploads"
app.config["PRODUCT_IMAGE_UPLOADS"] = "static\img\product"
app.secret_key = "12345"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/staff-home")
def staffhome():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * From accounts WHERE id = %s', (session['loginid'],))
        user = cursor.fetchone()

        return render_template("staff/index.html", activeuser=user)
    return redirect(url_for('login'))


@app.route('/staff-addproduct', methods=['GET', 'POST'])
def staffaddprod():
    cur = mysql.connection.cursor()
    userDict1 = {}
    u = shelve.open('user.db', 'r')
    userDict1 = u['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    createProductForm = CreateProductForm(request.form)
    if request.method == 'POST' and createProductForm.validate():
        productsDict = {}
        db = shelve.open('products.db', 'c')
        try:
            productsDict = db['products']
        except:
            print("Error in retrieving products from products.db")
        print(request.files, "file")
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOADS"], image.filename))

        productdetails = (createProductForm.Name.data,
                     createProductForm.Brand.data,
                     createProductForm.Category.data,
                     createProductForm.RetailPrice.data,
                     createProductForm.Quantity.data,
                     image.filename,
                     createProductForm.ListPrice.data,
                     "Active",
                     createProductForm.Member.data,
                     createProductForm.Sale.data,
                     createProductForm.SalePrice.data,
                     createProductForm.SaleStartDate.data,
                     createProductForm.SaleEndDate.data)

        print(productdetails)
        
        sql = 'Insert INTO product_table VALUES(NULL,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s ,%s)'
        cur.execute(sql,productdetails)
        mysql.connection.commit()

        return redirect(url_for('staffprod'))
    else:
        print("Failed adding to DB")
    print(createProductForm.validate())
    return render_template('staff/product-add.html', form=createProductForm, activeuser=activeuser)


@app.route('/staff-updateproduct/<int:id>/', methods=['GET', 'POST'])
def staffupdateprod(id):
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM product_table WHERE ProductID = %s"
    cur.execute(sql, (id,))
    pd = cur.fetchone()
    userDict1 = {}
    u = shelve.open('user.db', 'r')
    userDict1 = u['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    updateProductForm = CreateProductForm(request.form)
    if request.method == 'POST':
        productsdict = {}
        db = shelve.open('products.db', 'w')
        productsdict = db['products']
        # upload img
        image_name = ""
        if request.files:
            image = request.files["image"]
            image_name = pd["image"]

            image_name = image.filename
            image.save(os.path.join(app.config["PRODUCT_IMAGE_UPLOADS"], image_name))
        productdetails = (updateProductForm.Name.data,
                          updateProductForm.Brand.data,
                          updateProductForm.Category.data,
                          updateProductForm.RetailPrice.data,
                          updateProductForm.ListPrice.data,
                          updateProductForm.Quantity.data,
                          image.filename,
                          updateProductForm.Sale.data,
                          updateProductForm.SalePrice.data,
                          updateProductForm.SaleStartDate.data,
                          updateProductForm.SaleEndDate.data,
                          updateProductForm.Member.data,
                          id)
        # upload img - end
        print(updateProductForm.RetailPrice.data,'retail price')
        sql_update = "UPDATE product_table " \
                     "SET ProductName =%s, ProductBrand=%s, ProductCategory =%s,RetailPrice=%s, ListPrice=%s,Quantity =%s, image =%s,Sale= %s,SalePrice=%s,SaleStartDate=%s,SaleEndDate=%s,MemberOnly=%s WHERE ProductID = %s"
        cur.execute(sql_update,productdetails)
        mysql.connection.commit()

        return redirect(url_for('staffprod'))
    else:
        productsDict = {}
        db = shelve.open('products.db', 'r')
        productsDict = db['products']
        db.close()



        print(pd)
        print(productsDict)
        product = productsDict.get(id)

        updateProductForm.Name.data = pd["ProductName"]
        updateProductForm.Brand.data = pd["ProductBrand"]
        updateProductForm.Category.data = pd["ProductCategory"]
        updateProductForm.RetailPrice.data = pd["RetailPrice"]
        updateProductForm.ListPrice.data = pd["ListPrice"]
        updateProductForm.Quantity.data = pd["Quantity"]
        image = pd["image"]
        updateProductForm.Sale.data = pd["Sale"]
        updateProductForm.SalePrice.data = pd["SalePrice"]
        updateProductForm.SaleStartDate.data = pd["SaleStartDate"]
        updateProductForm.SaleEndDate.data = pd["SaleEndDate"]
        updateProductForm.Member.data = pd["MemberOnly"]
        print(product)

        return render_template('staff/product-update.html', form=updateProductForm, image=image, activeuser=activeuser)


@app.route('/ProductStatus/<int:id>', methods=['POST'])
def ProductStatus(id):
    productsDict = {}

    db = shelve.open('products.db', 'w')
    productsDict = db['products']
    cur = mysql.connection.cursor()
    sql = "SELECT Status FROM product_table WHERE ProductID = %s"
    cur.execute(sql, (id,))
    current = cur.fetchone()
    print(current)
    if current['Status'] == "Active":
        cur.execute('UPDATE product_table SET Status = "Inactive" WHERE ProductID = %s',(id,))
    else:
        cur.execute('UPDATE product_table SET Status = "Active" WHERE ProductID = %s',(id,))

    mysql.connection.commit()
    db['products'] = productsDict
    db.close()

    flash("Updated", "danger")
    return redirect(url_for('staffprod'))


@app.route('/staff-product')
def staffprod():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM product_table')
    products = cur.fetchall()

    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * From accounts WHERE id = %s', (session['loginid'],))
        user = cursor.fetchone()


    return render_template("staff/product.html", products=products, count=cur.rowcount,
                           activeuser=user)
    """
    usersDict = {}
    db = shelve.open('storage.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)
    return render_template('retrieveUsers.html',
                           usersList=usersList, count=len(usersList))
    """



@app.route("/staff-fullInv")
def staffinventoryoverview():
    return render_template("staff/fullinventory.html")


@app.route("/staff-stock")
def staffstock():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    for key in suppliersDict:
        supplier = suppliersDict.get(key)
        suppliersList.append(supplier)

    return render_template("staff/stock.html", suppliersList=suppliersList, count=len(suppliersList),
                           activeuser=activeuser)


@app.route("/staff-stockdetails")
def staffstockdetails():
    return render_template("staff/stockdetail.html")


@app.route("/staff-addsupplier", methods=["GET", "POST"])
def staffaddsupplier():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    addSupplierForm = AddSupplierForm(request.form)
    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    productsList = [("", "Select")]
    products = []
    for key in productsDict:
        product = productsDict.get(key)
        productsTuple = (product.get_productName(), product.get_productName())
        productsList.append(productsTuple)
        products.append(product)

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    for key in suppliersDict:
        supplier = suppliersDict.get(key)
        suppliersList.append(supplier)

    print(any(char.isdigit() for char in str(addSupplierForm.price.data)))
    addSupplierForm.product.choices = productsList

    if request.method == 'POST' and addSupplierForm.validate():
        suppliersDict = {}

        db = shelve.open('inventory.db', 'c')

        try:
            suppliersDict = db['Suppliers']
        except:
            print("Error in retrieving Suppliers from inventory.db.")

        supplierName = addSupplierForm.supplierName.data

        for supplier in suppliersList:
            if addSupplierForm.supplierName.data == supplier.get_supplier_name():
                flash("Supplier Name Already Exists", "NameError")
                return redirect(url_for("staffaddsupplier"))

        supplierAddress = addSupplierForm.supplierAddress.data

        for supplier in suppliersList:
            if addSupplierForm.supplierAddress.data == supplier.get_supplier_address():
                flash("Supplier Address Already Exists", "AddressError")
                return redirect(url_for("staffaddsupplier"))

        if len(addSupplierForm.supplierAddress.data) == 6:
            if addSupplierForm.supplierAddress.data[:-1].isdigit():
                supplierAddress = addSupplierForm.supplierAddress.data
        else:
            flash("Invalid Address", "AddressError")
            return redirect(url_for("staffaddsupplier"))

        supplierWebsite = addSupplierForm.website.data

        for supplier in suppliersList:
            if addSupplierForm.website.data == supplier.get_website():
                flash("Website Already Exists", "WebsiteError")
                return redirect(url_for("staffaddsupplier"))

        if addSupplierForm.website.data[0:4] == "www." and addSupplierForm.website.data[-4:] == ".com":
            supplierWebsite = addSupplierForm.website.data
        else:
            flash("Make sure it is written in the correct format (www.'name'.com)", "WebsiteError")
            return redirect(url_for("staffaddsupplier"))

        supplierPhone = addSupplierForm.phone.data

        for supplier in suppliersList:
            if addSupplierForm.phone.data == supplier.get_phone():
                flash("Phone Number Already In Use", "PhoneError")
                return redirect(url_for("staffaddsupplier"))

        if len(str(addSupplierForm.phone.data)) == 8:
            if str(addSupplierForm.phone.data)[0] == '9' or str(addSupplierForm.phone.data)[0] == '6' or \
                    str(addSupplierForm.phone.data)[0] == '8':
                supplierPhone = addSupplierForm.phone.data
        else:
            flash("Invalid Phone Number", "PhoneError")
            return redirect(url_for("staffaddsupplier"))

        for supplier in suppliersList:
            if addSupplierForm.contact.data == supplier.get_contact():
                flash("Contact Already In Use", "ContactError")
                return redirect(url_for("staffaddsupplier"))

        if any(char.isdigit() for char in addSupplierForm.contact.data) == False:
            supplierContact = addSupplierForm.contact.data
        else:
            flash("Invalid Contact", "ContactError")
            return redirect(url_for("staffaddsupplier"))

        supplierProduct = addSupplierForm.product.data

        if any(char.isdigit() for char in str(addSupplierForm.price.data)) == True:
            if addSupplierForm.price.data > 0:
                supplierPrice = addSupplierForm.price.data
        else:
            flash("Invalid Price", "PriceError")
            return redirect(url_for("staffaddsupplier"))

        supplier = Supplier.Supplier(supplierName, supplierAddress, supplierWebsite, supplierPhone, supplierContact,
                                     supplierProduct, supplierPrice)
        supplier.set_validity("Valid")
        for product in products:
            if product.get_productName() == supplierProduct:
                supplier.set_brand(product.get_productBrand())
                print(supplier.get_brand())

        suppliersDict[supplier.get_id()] = supplier

        db['Suppliers'] = suppliersDict
        db.close()

        return redirect(url_for('staffstock'))
    return render_template('staff/addSupplier.html', form=addSupplierForm, activeuser=activeuser)


@app.route('/staff-updateSupplier/<int:id>/', methods=['GET', 'POST'])
def updateSupplier(id):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    updateSupplierForm = AddSupplierForm(request.form)
    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    productsList = [("", "Select")]
    products = []
    for key in productsDict:
        product = productsDict.get(key)
        productsTuple = (product.get_productName(), product.get_productName())
        productsList.append(productsTuple)
        products.append(product)

    updateSupplierForm.product.choices = productsList

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    for key in suppliersDict:
        supplier = suppliersDict.get(key)
        suppliersList.append(supplier)

    if request.method == "POST" and updateSupplierForm.validate():
        suppliersDict = {}
        db = shelve.open("inventory.db", "w")
        suppliersDict = db["Suppliers"]

        supplier = suppliersDict.get(id)

        supplierName = updateSupplierForm.supplierName.data

        supplier.set_supplier_name(supplierName)

        supplierAddress = updateSupplierForm.supplierAddress.data

        if len(updateSupplierForm.supplierAddress.data) == 6:
            if updateSupplierForm.supplierAddress.data[:-1].isdigit():
                supplierAddress = updateSupplierForm.supplierAddress.data
        else:
            flash("Invalid Address", "AddressError")
            return redirect(url_for("updateSupplier", id=supplier.get_id()))

        supplier.set_supplier_address(supplierAddress)

        supplierWebsite = updateSupplierForm.website.data

        if updateSupplierForm.website.data[0:4] == "www." and updateSupplierForm.website.data[-4:] == ".com":
            supplierWebsite = updateSupplierForm.website.data
        else:
            flash("Make sure it is written in the correct format (www.'name'.com)", "WebsiteError")
            return redirect(url_for("updateSupplier", id=supplier.get_id()))

        supplier.set_website(supplierWebsite)

        supplierPhone = updateSupplierForm.phone.data

        if len(str(updateSupplierForm.phone.data)) == 8:
            if str(updateSupplierForm.phone.data)[0] == '9' or str(updateSupplierForm.phone.data)[0] == '6' or \
                    str(updateSupplierForm.phone.data)[0] == '8':
                supplierPhone = updateSupplierForm.phone.data
        else:
            flash("Invalid Phone Number", "PhoneError")
            return redirect(url_for("updateSupplier", id=supplier.get_id()))

        supplier.set_phone(supplierPhone)

        supplierContact = updateSupplierForm.contact.data

        if any(char.isdigit() for char in updateSupplierForm.contact.data) == False:
            supplierContact = updateSupplierForm.contact.data
        else:
            flash("Invalid Contact", "ContactError")
            return redirect(url_for("updateSupplier", id=supplier.get_id()))

        supplier.set_contact(supplierContact)

        supplierProduct = updateSupplierForm.product.data
        supplier.set_product(supplierProduct)
        for product in products:
            if product.get_productName() == supplierProduct:
                supplier.set_brand(product.get_productBrand())
                print(supplier.get_brand())

        supplierPrice = updateSupplierForm.price.data
        if any(char.isdigit() for char in str(updateSupplierForm.price.data)) == True:
            if updateSupplierForm.price.data > 0:
                supplierPrice = updateSupplierForm.price.data
        else:
            flash("Invalid Price", "PriceError")
            return redirect(url_for("updateSupplier", id=supplier.get_id()))
        supplier.set_price(supplierPrice)

        db["Suppliers"] = suppliersDict
        db.close()

        return redirect(url_for("staffstock"))
    else:
        suppliersDict = {}
        db = shelve.open("inventory.db", "r")
        suppliersDict = db["Suppliers"]
        db.close()

        supplier = suppliersDict.get(id)
        updateSupplierForm.supplierName.data = supplier.get_supplier_name()
        updateSupplierForm.supplierAddress.data = supplier.get_supplier_address()
        updateSupplierForm.website.data = supplier.get_website()
        print(updateSupplierForm.website.data[0:4])
        print(updateSupplierForm.website.data[-4:])
        updateSupplierForm.phone.data = supplier.get_phone()
        updateSupplierForm.contact.data = supplier.get_contact()
        updateSupplierForm.product.data = supplier.get_product()
        updateSupplierForm.price.data = supplier.get_price()

        return render_template('staff/updateSupplier.html', form=updateSupplierForm, activeuser=activeuser)


@app.route('/staff-supplier-details/<int:id>/', methods=['GET', 'POST'])
def supplierDetails(id):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    supplier = suppliersDict.get(id)
    suppliersList.append(supplier)

    return render_template("staff/supplierDetails.html", suppliersList=suppliersList, count=len(suppliersList),
                           activeuser=activeuser)


@app.route('/change-supplier-validity/<int:id>', methods=['POST'])
def changeValidity(id):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    suppliersDict = {}

    db = shelve.open('inventory.db', 'w')
    suppliersDict = db['Suppliers']

    supplier = suppliersDict.get(id)
    current = supplier.get_validity()
    if current == "Valid":
        supplier.set_validity("Invalid")
    else:
        supplier.set_validity("Valid")

    db['Suppliers'] = suppliersDict
    db.close()

    flash("Updated", "danger")
    return redirect(url_for('staffstock'))


@app.route('/staff-choose-supplier/<int:id>/', methods=['GET', 'POST'])
def chooseSupplier(id):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    productsList = []
    product = productsDict.get(id)
    productsList.append(product)

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    for key in suppliersDict:
        supplier = suppliersDict.get(key)
        suppliersList.append(supplier)

    return render_template("staff/chooseSupplier.html", suppliersList=suppliersList, productsList=productsList,
                           count=len(suppliersList), activeuser=activeuser)


@app.route("/staff-order")
def stafforderproduct():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    ordersDict = {}
    db = shelve.open('inventory.db', 'r')
    ordersDict = db['Orders']
    db.close()

    productsList = []
    for key in productsDict:
        product = productsDict.get(key)
        productsList.append(product)

    """
    orderedProduct = []
    for i in ordersDict:
        order = ordersDict.get(i)
        orderedProduct.append(order)
    """
    ordersList = []
    if len(ordersDict) > 0:
        for product in productsList:
            order = ordersDict.get(product.get_productName(), "Not Found")
            if order == "Not Found":
                c = []
                empty = Order.Order(product.get_productName())
                empty.set_status("Order")
                c.append(product)
                c.append(empty)
                ordersList.append(c)
            elif order != "Not Found":
                c = []
                c.append(product)
                c.append(order)
                ordersList.append(c)
    elif len(ordersDict) == 0:
        for product in productsList:
            c = []
            empty = Order.Order(product.get_productName())
            empty.set_status("Order")
            c.append(product)
            c.append(empty)
            ordersList.append(c)
    return render_template("staff/order.html", ordersList=ordersList, count=len(productsList), activeuser=activeuser)


@app.route('/staff-order-product/<int:sid>/<int:pid>', methods=['GET', 'POST'])
def orderProduct(sid, pid):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    addOrderForm = AddOrder(request.form)
    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    productsList = []
    product = productsDict.get(pid)
    productsList.append(product)

    suppliersDict = {}
    db = shelve.open('inventory.db', 'r')
    suppliersDict = db['Suppliers']
    db.close()

    suppliersList = []
    supplier = suppliersDict.get(sid)
    suppliersList.append(supplier)
    if request.method == "POST" and addOrderForm.validate():
        ordersDict = {}
        db = shelve.open('inventory.db', 'c')

        try:
            ordersDict = db['Orders']
        except:
            print("Error in retrieving Orders from inventory.db.")

        orderQuantity = addOrderForm.quantity.data

        date = datetime.now()

        orderDate = date.strftime("%x")

        orderTime = date.strftime("%X")

        order = Order.Order(productsList[0].get_productName())
        order.set_supplier(suppliersList[0])
        order.set_quantity(orderQuantity)
        order.set_date(orderDate)
        order.set_time(orderTime)
        order.set_status("Pending")
        print("Product:", order.get_product() + "\n" + "Supplier:", order.get_supplier().get_supplier_name() + "\n")
        ordersDict[order.get_product()] = order
        print(ordersDict[order.get_product()].get_product())
        db['Orders'] = ordersDict

        db.close()

        return redirect(url_for('stafforderproduct'))
    else:
        return render_template("staff/orderProduct.html", suppliersList=suppliersList, productsList=productsList,
                               count=len(suppliersList), form=addOrderForm, activeuser=activeuser)


@app.route("/staff-pending-order/<int:oid>/<int:pid>", methods=['GET', 'POST'])
def orderPending(oid, pid):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    ordersDict = {}
    db = shelve.open('inventory.db', 'r')
    ordersDict = db['Orders']
    db.close()

    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    productsList = []
    product = productsDict.get(pid)
    productsList.append(product)

    ordersList = []
    order = ordersDict.get(product.get_productName())
    ordersList.append(order)

    orderStatusForm = OrderStatus(request.form)
    if request.method == "POST" and orderStatusForm.validate():
        status = orderStatusForm.status.data

        if status == "D":
            productsList[0].add_stock(ordersList[0].get_quantity())
            productsDict[productsList[0].get_productID()] = productsList[0]
            db = shelve.open('products.db', 'w')
            db['products'] = productsDict
            db.close()

            try:
                del ordersDict[ordersList[0].get_product()]
            except KeyError:
                print("Error finding order")

            db = shelve.open('inventory.db', 'w')
            db['Orders'] = ordersDict
            db.close()

        return redirect(url_for('stafforderproduct'))
    else:
        return render_template("staff/orderDetails.html", ordersList=ordersList, count=len(ordersList),
                               form=orderStatusForm, activeuser=activeuser)


@app.route("/staff-addstock")
def staffaddstock():
    return render_template("staff/addstock.html")


@app.route("/staff-invHome")
def staffinvHome():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    return render_template("staff/invHome.html", activeuser=activeuser)


@app.route("/staff-report")
def staffreport():
    return render_template("staff/detailedreport.html")


@app.route("/staff-actinfo")
def staffactinfo():
    '''
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['loginid'],))
    user = cursor.fetchone()

    cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursors.execute('Select * FROM accounts')
    accounts = cursors


    return render_template('staff/accountinfo.html', activeuser=user, accounts=accounts,
                           loginUser=session.get('loginUser'), count=cursors.rowcount)


@app.route('/UpdatePassword/<int:id>/', methods=['GET', 'POST'])
def UpdatePassword(id):
    '''
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    '''
    error = None
    updatePasswordForm = changepassword(request.form)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    print(session.get('loginUser'))
    account = cursor.fetchone()
    if request.method == 'POST' and updatePasswordForm.validate():
        '''
        userDict = {}
        db = shelve.open('user.db', 'w')
        userDict = db['Users']

        user = userDict.get(id)
        '''

        if updatePasswordForm.newpassword.data == updatePasswordForm.passwordRepeat.data:
            updatePasswordForm.newpassword.data = updatePasswordForm.newpassword.data
            '''
            user.set_password(updatePasswordForm.newpassword.data)
            db['Users'] = userDict
            db.close()
            '''
            cursorss = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursorss.execute('UPDATE accounts SET password = %s WHERE id = %s',
                             (updatePasswordForm.newpassword.data, id))
            mysql.connection.commit()

            return redirect(url_for('staffactinfo', activeuser=account))
        else:
            error = 'New password does not match confirm password'
            return render_template('staff/UpdatePassword.html', form=updatePasswordForm, error=error,
                                   activeuser=account)



    else:
        '''
        userDict = {}
        db = shelve.open('user.db', 'r')
        userDict = db['Users']

        db.close()
        user = userDict.get(id)
        '''
        cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursors.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        user = cursors.fetchone()

        return render_template('staff/UpdatePassword.html', form=updatePasswordForm, activeuser=account)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = userchangeinfo(request.form)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    print(session.get('loginUser'))
    account = cursor.fetchone()

    if request.method == 'POST' and updateUserForm.validate():

        cursorss = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursorss.execute('UPDATE accounts SET email = %s,type=%s WHERE id = %s',
                         (updateUserForm.email.data, updateUserForm.accounttype.data, id))
        mysql.connection.commit()
        return redirect(url_for('staffactinfo'))
    else:
        cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursors.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        user = cursors.fetchone()

        updateUserForm.firstName.data = user['firstname']
        updateUserForm.lastName.data = user['lastname']
        updateUserForm.gender.data = user['gender']
        updateUserForm.email.data = user['email']
        updateUserForm.phone.data = user['phone']
        updateUserForm.city.data = user['city']
        updateUserForm.address.data = user['address']
        updateUserForm.unit.data = user['unit']
        updateUserForm.postal.data = user['postal']
        updateUserForm.accounttype.data = user['type']
        return render_template('staff/updateUser.html', form=updateUserForm, activeuser=account)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    '''
    usersDict = {}
    db = shelve.open('user.db', 'w')
    usersDict = db['Users']
    usersDict.pop(id)

    db['Users'] = usersDict
    db.close()
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    print(session.get('loginUser'))
    account = cursor.fetchone()

    cursorss = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorss.execute('DELETE FROM accounts WHERE id = %s',
                     (id,))
    mysql.connection.commit()

    return redirect(url_for('staffactinfo'))


@app.route('/UpdateStaffAccount', methods=['GET', 'POST'])
def UpdateStaffAccount():
    ''''
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    account = cursor.fetchone()

    userDict = {}
    db = shelve.open('user.db', 'w')
    userDict = db['Users']
    user = userDict.get(session.get('loginUser'))
    print(user.get_firstName())

    updateAccountForm = userchangeinfo(request.form)
    if request.method == 'POST' and updateAccountForm.validate():
        print(updateAccountForm.gender.data)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'UPDATE accounts SET firstname = %s, lastname = %s, gender = %s, email = %s, phone = %s, city = %s, address = %s , unit =%s, postal=%s WHERE id = %s',
            (updateAccountForm.firstName.data, updateAccountForm.lastName.data, updateAccountForm.gender.data,
             updateAccountForm.email.data, updateAccountForm.phone.data, updateAccountForm.city.data,
             updateAccountForm.address.data, updateAccountForm.unit.data, updateAccountForm.postal.data, account['id']))
        mysql.connection.commit()
        '''
        user.set_firstName(updateAccountForm.firstName.data)
        user.set_lastName(updateAccountForm.lastName.data)
        user.set_gender(updateAccountForm.gender.data)
        user.set_email(updateAccountForm.email.data)
        user.set_phone(updateAccountForm.phone.data)
        user.set_city(updateAccountForm.city.data)
        user.set_address(updateAccountForm.address.data)
        user.set_unit(updateAccountForm.unit.data)
        user.set_postal(updateAccountForm.postal.data)

        db['Users'] = userDict

        db.close()
        '''

        return redirect(url_for('staffhome'))
    else:
        '''
        userDict = {}
        db = shelve.open('user.db', 'r')
        userDict = db['Users']
        db.close()
        '''

        updateAccountForm.firstName.data = account['firstname']
        updateAccountForm.lastName.data = account['lastname']
        updateAccountForm.gender.data = account['gender']
        updateAccountForm.email.data = account['email']
        updateAccountForm.phone.data = account['phone']
        updateAccountForm.city.data = account['city']
        updateAccountForm.address.data = account['address']
        updateAccountForm.unit.data = account['unit']
        updateAccountForm.postal.data = account['postal']

    return render_template('staff/UpdateStaffAccount.html', user=user, activeuser=account,
                           loginUser=session.get('loginUser'), form=updateAccountForm)


@app.route('/UpdateAccount', methods=['GET', 'POST'])
def UpdateAccount():
    userDict = {}
    db = shelve.open('user.db', 'w')
    userDict = db['Users']
    user = userDict.get(session.get('loginUser'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['loginid'],))
    account = cursor.fetchone()
    print(account)

    updateAccountForm = userchangeinfo(request.form)
    if request.method == 'POST' and updateAccountForm.validate():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'UPDATE accounts SET firstname = %s, lastname = %s, gender = %s, email = %s, phone = %s, city = %s, address = %s , unit =%s, postal=%s WHERE id = %s',
            (updateAccountForm.firstName.data, updateAccountForm.lastName.data, updateAccountForm.gender.data,
             updateAccountForm.email.data, updateAccountForm.phone.data, updateAccountForm.city.data,
             updateAccountForm.address.data, updateAccountForm.unit.data, updateAccountForm.postal.data, account['id']))
        mysql.connection.commit()
        return redirect(url_for('useraccount'))
    else:
        updateAccountForm.firstName.data = account['firstname']
        updateAccountForm.lastName.data = account['lastname']
        updateAccountForm.gender.data = account['gender']
        updateAccountForm.email.data = account['email']
        updateAccountForm.phone.data = account['phone']
        updateAccountForm.city.data = account['city']
        updateAccountForm.address.data = account['address']
        updateAccountForm.unit.data = account['unit']
        updateAccountForm.postal.data = account['postal']
    return render_template('UpdateAccount.html', form=updateAccountForm)


@app.route('/UpdateStaffPassword', methods=['GET', 'POST'])
def UpdateStaffPassword():
    '''
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    '''

    userDict = {}
    db = shelve.open('user.db', 'w')
    userDict = db['Users']
    user = userDict.get(session.get('loginUser'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    account = cursor.fetchone()

    updateAccountForm = userchangepassword(request.form)
    if request.method == 'POST' and updateAccountForm.validate():
        if updateAccountForm.oldpassword.data == account['password']:
            if updateAccountForm.newpassword.data == updateAccountForm.passwordRepeat.data:
                updateAccountForm.newpassword.data = updateAccountForm.newpassword.data
                '''
                user.set_password(updateAccountForm.newpassword.data)
                '''
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                    'UPDATE accounts SET password = %s WHERE id = %s',
                    (updateAccountForm.newpassword.data, account['id']))
                mysql.connection.commit()

            else:
                error = 'New password does not match confirm password'
                return render_template('staff/UpdateStaffPassword.html', error=error, form=updateAccountForm,
                                       activeuser=account)
        else:
            error = 'Wrong current password'
            return render_template('staff/UpdateStaffPassword.html', error=error, form=updateAccountForm,
                                   activeuser=account)

        db['Users'] = userDict

        db.close()
        return redirect(url_for('staffhome'))

    return render_template('staff/UpdateStaffPassword.html', user=user, activeuser=account,
                           loginUser=session.get('loginUser'), form=updateAccountForm)


@app.route('/UserUpdatePassword', methods=['GET', 'POST'])
def UserUpdatePassword():
    '''
    userDict = {}
    db = shelve.open('user.db', 'w')
    userDict = db['Users']
    user = userDict.get(session.get('loginUser'))
    '''

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    account = cursor.fetchone()

    updateAccountForm = userchangepassword(request.form)
    if request.method == 'POST' and updateAccountForm.validate():
        if updateAccountForm.oldpassword.data == account['password']:
            if updateAccountForm.newpassword.data == updateAccountForm.passwordRepeat.data:
                updateAccountForm.newpassword.data = updateAccountForm.newpassword.data
                '''
                user.set_password(updateAccountForm.newpassword.data)
                '''
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(
                    'UPDATE accounts SET password = %s WHERE id = %s',
                    (updateAccountForm.newpassword.data, account['id']))
                mysql.connection.commit()

            else:
                error = 'New password does not match confirm password'
                return render_template('UserUpdatePassword.html', error=error, form=updateAccountForm)
        else:
            error = 'Wrong current password'
            return render_template('UserUpdatePassword.html', error=error, form=updateAccountForm)

        return redirect(url_for('useraccount'))

    return render_template('UserUpdatePassword.html', activeuser=account, loginUser=session.get('loginUser'),
                           form=updateAccountForm)


@app.route("/AccountChart")
def AccountChart():
    '''
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))
    '''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session.get('loginUser'),))
    account = cursor.fetchone()

    '''
    db = shelve.open("user.db", "r")
    quanDict = {}
    quanDict = db["Users"]
    db.close()
    '''
    cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursors.execute('Select date FROM accounts')
    accounts = cursors
    print(accounts)

    janlist = []
    feblist = []
    marlist = []
    aprlist = []
    maylist = []
    junlist = []
    jullist = []
    auglist = []
    seplist = []
    octlist = []
    novlist = []
    declist = []
    '''
    for key in quanDict:
        count = quanDict.get(key)
        d = str(count.get_date())
        datesplit = d.split('-')
        print(datesplit)
    '''
    for key in accounts:
        print(key)
        d = str(key)
        datesplit = d.split('-')

        if datesplit[1] == "01":
            janlist.append(key)

        if datesplit[1] == "02":
            feblist.append(key)

        if datesplit[1] == "03":
            marlist.append(key)

        if datesplit[1] == "04":
            aprlist.append(key)

        if datesplit[1] == "05":
            maylist.append(key)

        if datesplit[1] == "06":
            junlist.append(key)

        if datesplit[1] == "07":
            jullist.append(key)

        if datesplit[1] == "08":
            auglist.append(key)

        if datesplit[1] == "09":
            seplist.append(key)

        if datesplit[1] == "10":
            octlist.append(key)

        if datesplit[1] == "11":
            novlist.append(key)

        if datesplit[1] == "12":
            declist.append(key)

    today = date.today()
    todays = str(today)
    todayt = todays.split('-')
    if todayt[1] == '01':
        labels = ['FEB', 'MAR', 'APR',
                  'MAY', 'JUN', 'JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN']
        values = [len(feblist), len(marlist), len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist)]

    elif todayt[1] == '02':
        labels = ['MAR', 'APR',
                  'MAY', 'JUN', 'JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB']
        values = [len(marlist), len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist)]
    elif todayt[1] == '03':
        labels = ['APR',
                  'MAY', 'JUN', 'JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR']
        values = [len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist)]
    elif todayt[1] == '04':
        labels = ['MAY', 'JUN', 'JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR']
        values = [len(maylist), len(junlist), len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist)]
    elif todayt[1] == '05':
        labels = ['JUN', 'JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY']
        values = [len(junlist), len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist)]
    elif todayt[1] == '06':
        labels = ['JUL', 'AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN']
        values = [len(jullist), len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist)]
    elif todayt[1] == '07':
        labels = ['AUG',
                  'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL']
        values = [len(auglist),
                  len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist)]
    elif todayt[1] == '08':
        labels = ['SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', ]
        values = [len(seplist), len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist)]
    elif todayt[1] == '09':
        labels = ['OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP']
        values = [len(octlist), len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist), len(seplist)]
    elif todayt[1] == '10':
        labels = ['NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT']
        values = [len(novlist), len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist), len(seplist), len(octlist)]
    elif todayt[1] == '11':
        labels = ['DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV']
        values = [len(declist), len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist), len(seplist), len(octlist),
                  len(novlist)]
    elif todayt[1] == '12':
        labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        values = [len(janlist), len(feblist), len(marlist),
                  len(aprlist), len(maylist), len(junlist), len(jullist), len(auglist), len(seplist), len(octlist),
                  len(novlist), len(declist)]

    bar_labels = labels
    bar_values = values

    return render_template('staff/AccountChart.html', title='User creation- Statistics(Graph)', activeuser=account,
                           max=50, labels=bar_labels, values=bar_values, JanList=janlist, FebList=feblist,
                           MarList=marlist, AprList=aprlist, MayList=maylist, JunList=junlist, JulList=jullist,
                           AugList=auglist, SepList=seplist, OctList=octlist, NovList=novlist, DecList=declist,
                           jancount=len(janlist), febcount=len(feblist), marcount=len(marlist), aprcount=len(aprlist),
                           maycount=len(maylist), juncount=len(junlist), julcount=len(jullist), augcount=len(auglist),
                           sepcount=len(seplist), octcount=len(octlist), novcount=len(novlist), deccount=len(declist))


@app.route("/staff-purhist")
def staffpurhist():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    return render_template("staff/purchasehistory.html", activeuser=activeuser)


@app.route("/staff-sales")
def staffsales():
    userDict1 = {}
    db = shelve.open('user.db', 'c')
    s = shelve.open('sale_storage.db', 'c')

    saleDict = {}
    try:
        userDict1 = db['Users']

        saleDict = s['sale']
    except:
        print("No Sales")
    s.close()
    activeuser = userDict1.get(session.get('loginUser'))
    print(userDict1)

    refundDict = {}
    rdb = shelve.open('refund_storage.db', 'c')
    try:
        refundDict = rdb['refund']
    except:
        print("Error in retrieving Users from refund_storage.db.")
    rdb['refund'] = refundDict
    rdb.close()

    refundList = []
    for key in refundDict:
        refund = refundDict.get(key)
        refundList.append(refund)

    saleList = []
    for key in saleDict:
        sale = saleDict.get(key)
        saleList.append(sale)

    OTSDict = {}

    for i in saleList:
        for product in i.get_purchases():
            if product.get_productName() not in OTSDict.keys():
                OTSDict[product.get_productName()] = [product.get_quantity(),
                                                      (int(product.get_quantity()) * int(product.totalprice()))]
            elif product.get_productName() in OTSDict.keys():
                OTSDict[product.get_productName()][0] += product.get_quantity()
                OTSDict[product.get_productName()][1] += (int(product.get_quantity()) * int(product.totalprice()))

    MTPSDict = {}
    tdate = date.today()
    today = tdate.strftime('%Y-%m-%d').replace('-', '')
    month = today[4:6]

    for i in saleList:
        for product in i.get_purchases():
            odate = i.get_sales_date()
            sdate = odate.strftime('%Y-%m-%d').replace('-', '')
            salemonth = sdate[4:6]
            if salemonth not in MTPSDict.keys():
                MTPSDict[salemonth] = {
                    product.get_productName(): (int(product.get_quantity()) * int(product.totalprice()))}
            elif salemonth in MTPSDict.keys():
                if product.get_productName() in MTPSDict[salemonth].keys():
                    MTPSDict[salemonth][product.get_productName()] += (
                                int(product.get_quantity()) * int(product.totalprice()))
                elif product.get_productName() not in MTPSDict[salemonth].keys():
                    MTPSDict[salemonth][product.get_productName()] = (
                                int(product.get_quantity()) * int(product.totalprice()))

    MMSPDict = {}

    for i in saleList:
        for product in i.get_purchases():
            odate = i.get_sales_date()
            sdate = odate.strftime('%Y-%m-%d').replace('-', '')
            salemonth = sdate[4:6]
            if salemonth not in MMSPDict.keys():
                MMSPDict[salemonth] = {product.get_productName(): product.get_quantity()}
            elif salemonth in MMSPDict.keys():
                if product.get_productName() in MMSPDict[salemonth].keys():
                    MMSPDict[salemonth][product.get_productName()] += product.get_quantity()
                elif product.get_productName() not in MMSPDict[salemonth].keys():
                    MMSPDict[salemonth][product.get_productName()] = product.get_quantity()

    labels = []
    jansale = []
    febsale = []
    marsale = []
    aprsale = []
    maysale = []
    junsale = []
    julsale = []
    augsale = []
    sepsale = []
    octsale = []
    novsale = []
    decsale = []
    data = []

    datadict = {}
    for i in saleList:
        for product in i.get_purchases():
            odate = i.get_sales_date()
            sdate = odate.strftime('%Y-%m-%d').replace('-', '')
            salemonth = sdate[4:6]
            if salemonth not in datadict.keys():
                datadict[salemonth] = (int(product.get_quantity()) * int(product.totalprice()))
            elif salemonth in datadict.keys():
                datadict[salemonth] += (int(product.get_quantity()) * int(product.totalprice()))

    for key in datadict:
        saletotal = datadict[key]
        if key == '01':
            jansale.append(saletotal)
        elif key == '02':
            febsale.append(saletotal)
            print(febsale)
        elif key == '03':
            marsale.append(saletotal)
        elif key == '04':
            aprsale.append(saletotal)
        elif key == '05':
            maysale.append(saletotal)
        elif key == '06':
            junsale.append(saletotal)
        elif key == '07':
            julsale.append(saletotal)
        elif key == '08':
            augsale.append(saletotal)
        elif key == '09':
            sepsale.append(saletotal)
        elif key == '10':
            octsale.append(saletotal)
        elif key == '11':
            novsale.append(saletotal)
        elif key == '12':
            decsale.append(saletotal)

    if month == '01':
        labels = ['Aug', 'Sept', 'Oct', 'Nov', 'Dec', 'Jan']
        data = [augsale, sepsale, octsale, novsale, decsale, jansale]
    elif month == '02':
        labels = ['Sept', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        data = [sepsale, octsale, novsale, decsale, jansale, febsale]
    elif month == '03':
        labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        data = [octsale, novsale, decsale, jansale, febsale, marsale]
    elif month == '04':
        labels = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
        data = [novsale, decsale, jansale, febsale, marsale, aprsale]
    elif month == '05':
        labels = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
        data = [decsale, jansale, febsale, marsale, aprsale, maysale]
    elif month == '06':
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        data = [jansale, febsale, marsale, aprsale, maysale, junsale]
    elif month == '07':
        labels = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        data = [febsale, marsale, aprsale, maysale, junsale, julsale]
    elif month == '08':
        labels = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        data = [marsale, aprsale, maysale, junsale, julsale, augsale]
    elif month == '09':
        labels = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept']
        data = [aprsale, maysale, junsale, julsale, augsale, sepsale]
    elif month == '10':
        labels = ['May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct']
        data = [maysale, junsale, julsale, augsale, sepsale, octsale]
    elif month == '11':
        labels = ['Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov']
        data = [junsale, julsale, augsale, sepsale, octsale, novsale]
    elif month == '12':
        labels = ['Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        data = [julsale, augsale, sepsale, octsale, novsale, decsale]

    return render_template("staff/sales.html", saleList=saleList, refundList=refundList, OTSDict=OTSDict,
                           MTPSDict=MTPSDict, MMSPDict=MMSPDict, tdate=tdate,
                           month=month, labels=labels, data=data, activeuser=activeuser)


@app.route("/refund")
def refund():
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    saleDict = {}
    s = shelve.open('sale_storage.db', 'r')
    saleDict = s['sale']
    s.close()

    saleList = []
    for key in saleDict:
        sale = saleDict.get(key)
        saleList.append(sale)

    return render_template("staff/refund.html", saleList=saleList, activeuser=activeuser)


@app.route('/refund-form/<int:id>/', methods=['GET', 'POST'])
def refund_form(id):
    userDict1 = {}
    db = shelve.open('user.db', 'r')
    userDict1 = db['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    refundform = Refund(request.form)
    if request.method == 'POST' and refundform.validate():
        salesDict = {}
        db = shelve.open('sale_storage.db', 'w')
        salesDict = db['sale']

        refundList = []
        refundDict = {}
        refund_db = shelve.open('refund_storage.db', 'w')
        refundDict = refund_db['refund']
        refundList = db['sale']
        refundDict[id] = refundList[id]
        refundList.pop(id)
        db['sale'] = refundList
        db.close()

        refund = refundDict.get(id)
        refund.set_refund_reason(refundform.refund_reason.data)
        refund.set_refund_status('Refunded')

        refund_db['refund'] = refundDict
        refund_db.close()

        '''
        sale = salesDict.get(id)
        sale.set_refund_reason(refundform.refund_reason.data)
        sale.set_refund_status('Refunded')

        db['sale'] = salesDict
        db.close()
        '''

        return redirect(url_for('staffsales'))
    else:
        salesDict = {}
        db = shelve.open('sale_storage.db', 'r')
        salesDict = db['sale']
        db.close()
        sale = salesDict.get(id)
        Refund.refund_reason = sale.get_refund_reason()
        Refund.refund_status = sale.get_refund_status()

        return render_template('staff/refund-form.html', sale=sale, form=refundform, activeuser=activeuser)


@app.route("/staff-sales_run")
def staffsalesrun():
    return render_template("staff/runsales.html")


@app.route("/staff-rewards", methods=['GET', 'POST'])
def staffrewards():  # staff rewards

    userDict1 = {}
    udb = shelve.open('user.db', 'r')
    userDict1 = udb['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    RewardsDict = {}
    invalid_rewards = {}
    db = shelve.open('RewardStorage.db', 'c')

    try:
        RewardsDict = db['Rewards']
    except:
        print("RewardsDict = db['Rewards'] error")
    try:
        invalid_rewards = db['Invalid_Rewards']
    except:
        print('Error retreiving invalid rewards')

    db.close()
    invalid_rewards_list = []
    RewardsList = []

    for key in invalid_rewards:
        Reward = invalid_rewards.get(key)
        invalid_rewards_list.append(Reward)

    for key in RewardsDict:
        Reward = RewardsDict.get(key)
        RewardsList.append(Reward)

    Length = len(RewardsList)
    return render_template('staff/Rewards.html', RewardsList=RewardsList, Length=Length,
                           invalid_rewards_list=invalid_rewards_list, activeuser=activeuser)


@app.route("/staff-addReward", methods=['GET', 'POST'])
def addrewards():
    userDict1 = {}
    udb = shelve.open('user.db', 'r')
    userDict1 = udb['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    createRewards = RewardsForm(request.form)

    if request.method == 'POST' and createRewards.validate():
        db = shelve.open('RewardStorage.db', 'c')
        RewardsDict = {}
        try:
            RewardsDict = db['Rewards']
        except:
            print('Error retrieving Rewards')

        if createRewards.Reward_Name.data in RewardsDict:
            flash("A reward with that name already exists", "nameError")
            return redirect(url_for('addrewards'))

        # upload img
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                flash('*Please Select an image', "imageError")
                return redirect(url_for('addrewards'))

            if os.path.exists('static/img/RewardsPicUploads/' + image.filename):
                flash('*Image name is currently used by another reward', "imageError")
                return redirect(url_for('addrewards'))

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

        # upload img - end

        Reward = RewardsClass.Reward(createRewards.Reward_Name.data, createRewards.Reward_Cost.data,
                                     createRewards.Reward_Desc.data, image.filename, createRewards.Reward_Category.data)
        RewardsDict[Reward.get_name()] = Reward
        db['Rewards'] = RewardsDict

        # test codes
        RewardsDict = db['Rewards']
        Reward = RewardsDict[Reward.get_name()]
        print(Reward.get_name(), 'was stored successfully with the key of', Reward.get_name())
        db.close()

        return redirect(url_for('staffrewards'))
    return render_template("staff/addReward.html", form=createRewards, activeuser=activeuser)


@app.route('/running-shoe/<int:id>')
def running_shoe(id):
    print(request.args)
    productsDict = {}
    db = shelve.open('products.db', 'r')
    productsDict = db['products']
    db.close()

    product = productsDict.get(id)
    print(id)
    print(product)
    print(productsDict)
    saleprice = product.get_ListPrice()
    if product.get_sale_status():
        saleprice = product.get_sale_price()

    return render_template("/running/running-shoe.html", product=product, saleprice=saleprice)


@app.route('/category')
def category():
    return render_template('category.html')


@app.route('/running-cat')
def running_cat():
    productsDict = {}
    db = shelve.open('products.db', 'r')
    userDict1 = {}
    membership = False
    activeuser = ''
    try:
        udb = shelve.open('user.db', 'r')
        userDict1 = udb['Users']
        activeuser = userDict1.get(session.get('loginUser'))
        if activeuser.get_accounttype() == "User":
            membership = True
    except:
        print("Not member")

    print(db)
    productsDict = db['products']
    db.close()

    productsList = []
    membersproductList = []

    for key in productsDict:
        product = productsDict.get(key)
        if product.get_memberOnly() == False:
            productsList.append(product)
            print(product.get_sale_status())
            saleprice = product.get_ListPrice()
            if product.get_sale_status():
                saleprice = product.get_sale_price()
                if not product.get_sale_Start_date() <= date.today() <= product.get_sale_End_date():
                    product.set_sale_status(False)
        print(product.get_image(), "image")

    for key in productsDict:
        product = productsDict.get(key)
        membersproductList.append(product)
        print(product.get_sale_status())
        saleprice = product.get_ListPrice()
        if product.get_sale_status():
            saleprice = product.get_sale_price()
            if not product.get_sale_Start_date() <= date.today() <= product.get_sale_End_date():
                product.set_sale_status(False)
    print(membership)
    print(productsList, "nonmbember")
    print(membersproductList, "member")

    return render_template('Running-Cat.html', productsList=productsList, count=len(productsList),
                           Sale=product.get_sale_status(), saleprice=saleprice,
                           memberList=membersproductList, activeuser=activeuser, membership=membership)


@app.route('/addtocart/<int:id>')
def addtocart(id):
    productsDict = {}
    cart = []
    currentList = []
    db = shelve.open('products.db', 'r')
    cartdb = shelve.open('cart_storage.db', 'c')
    productsDict = db['products']
    try:
        cart = cartdb['cart']
        currentList = cartdb['cartlist']
    except:
        print("NO CART")

    product = productsDict.get(id)
    print(product.get_ListPrice())
    item = product
    item.set_quantity(1)
    print(item)
    print(Product.Product.countID, "CountID")
    print(item.get_productID() in cart, 'hi')

    print(currentList, "ye")
    print(item.get_productID() in currentList)
    if item.get_productID() in currentList:
        for x in cart:
            if item.get_productID() == x.get_productID():
                x.set_quantity(int(x.get_quantity()) + 1)

    else:
        cart.append(item)

    currentList.append(item.get_productID())

    cartdb['cart'] = cart
    cartdb['cartlist'] = currentList
    print(cart, "test")
    for i in cart:
        print(i)
    print(cartdb['cart'],"cart")
    cartdb.close()
    db.close()
    return redirect(url_for('running_cat'))


@app.route('/single-product')
def singleproduct():
    return render_template('single-product.html')


@app.route('/cart')
def cart():
    updatecartform = UpdateCart(request.form)

    productList = []
    try:
        s = shelve.open('cart_storage.db', 'r')
        productList = s['cart']
        s.close()

    except:
        print('No Cart Storage!')

    subtotal = []
    for product in productList:
        print(product.get_productID())
        subtotal.append(int(product.get_quantity()) * int(product.totalprice()))

    return render_template('cart.html', productList=productList, subtotal=subtotal, form=updatecartform,
                           count=len(productList))


@app.route('/updateCart/<int:id>', methods=['POST'])
def updateCart(id):
    updatecartform = UpdateCart(request.form)
    productsDict = {}
    cartList = []

    p = shelve.open('products.db', 'r')
    db = shelve.open('cart_storage.db', 'c')

    cartList = db['cart']
    productsDict = p['products']
    product = productsDict.get(id)
    for x in cartList:
        if product.get_productID() == x.get_productID():
            x.set_quantity(updatecartform.updateqty.data)

    db['cart'] = cartList
    db.close()
    return redirect(url_for('cart'))


@app.route('/deleteCart/<int:id>', methods=['POST'])
def deleteCart(id):
    cart = []
    cartlist = []
    db = shelve.open('cart_storage.db', 'c')
    cart = db['cart']
    cartlist = db['cartlist']
    cart.pop(id)
    cartlist.pop(id)
    db['cart'] = cart
    db['cartlist'] = cartlist
    print(cart, "hi")
    db.close()
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    userDict = {}
    try:
        udb = shelve.open('user.db', 'c')
        userDict = udb['Users']
    except:
        print("NO USER")
    user = userDict.get(session.get('loginUser'))
    updateAccountForm = userchangeinfo(request.form)
    if request.method == 'POST' and updateAccountForm.validate():

        print(updateAccountForm.firstName.data)
        user.set_firstName(updateAccountForm.firstName.data)
        user.set_lastName(updateAccountForm.lastName.data)
        user.set_email(updateAccountForm.email.data)
        user.set_gender(updateAccountForm.gender.data)
        user.set_phone(updateAccountForm.phone.data)
        user.set_city(updateAccountForm.city.data)
        user.set_address(updateAccountForm.address.data)
        user.set_unit(updateAccountForm.unit.data)
        user.set_postal(updateAccountForm.postal.data)

        udb['Users'] = userDict

        udb.close()

        return redirect(url_for('checkout_creditcard'))
    else:
        try:
            userDict = {}
            db = shelve.open('user.db', 'r')
            userDict = db['Users']
            db.close()

            updateAccountForm.firstName.data = user.get_firstName()
            updateAccountForm.lastName.data = user.get_lastName()
            updateAccountForm.gender.data = user.get_gender()
            updateAccountForm.email.data = user.get_email()
            updateAccountForm.phone.data = user.get_phone()
            updateAccountForm.city.data = user.get_city()
            updateAccountForm.address.data = user.get_address()
            updateAccountForm.unit.data = user.get_unit()
            updateAccountForm.postal.data = user.get_postal()
        except:
            print("No USER")
    productList = []
    s = shelve.open('cart_storage.db', 'r')
    productList = s['cart']
    s.close()

    subtotal = []
    for product in productList:
        subtotal.append(int(product.get_quantity()) * int(product.totalprice()))

    return render_template('checkout.html', productList=productList, subtotal=subtotal, form=updateAccountForm,
                           count=len(productList), user=user, loginUser=session.get('loginUser'))


@app.route('/checkoutcreditcard', methods=['GET', 'POST'])
def checkout_creditcard():
    creditcard = CreditCard(request.form)
    if request.method == 'POST' and creditcard.validate():
        productList = []
        s = shelve.open('cart_storage.db', 'r')
        productList = s['cart']
        s.close()

        '''
        control year expiry range by 3
        d = date.today()
        f = d.strftime('%Y-%m-%d').replace('-', '')
        year = int(f[0:4])
        year1 = year + 1
        year2 = year + 2
        yearlist = []
        yearlist.append(str(year))
        yearlist.append(str(year1))
        yearlist.append(str(year2))
        '''

        subtotal = []
        for product in productList:
            subtotal.append(int(product.get_quantity()) * int(product.totalprice()))
        return redirect(url_for('confirmation'))

    return render_template('checkout_creditcard.html', form=creditcard)


@app.route('/confirmation')
def confirmation():
    purchaseList = []
    s = shelve.open('cart_storage.db', 'c')
    p = shelve.open('products.db', 'c')
    productsDict = {}

    try:
        productsDict = p['products']
        purchaseList = s['cart']
    except:
        print("ERROR")

    sale_date = date.today()

    # date for order number
    tdate = date.today()
    today = tdate.strftime('%Y-%m-%d').replace('-', '')

    #validate sale is valid before creation
    subtotal = []
    for purchase in purchaseList:
        subtotal.append(int(purchase.get_quantity()) * int(purchase.totalprice()))
    saletotal = sum(subtotal)

    if saletotal == 0:
        return redirect(url_for('cart'))

    else:
        sale = Sales.Sales(sale_date)
        sale.set_purchases(purchaseList)
        sale_id = sale.get_salesID()

        saleDict = {}
        sale_db = shelve.open('sale_storage.db', 'c')

        try:
            saleDict = sale_db['sale']
        except:
            print("Error in retrieving sales from sale_storage.db.")
        saleDict[sale_id] = sale
        sale_db['sale'] = saleDict
        sale_db.close()

        subtotal = []
        for purchase in purchaseList:
            subtotal.append(int(purchase.get_quantity()) * int(purchase.totalprice()))
            for key in productsDict:
                product = productsDict.get(key)
                print(purchase, "PuR")
                print(product, "PRO")
                print(product.get_productID() == purchase.get_productID())
                if product.get_productID() == purchase.get_productID():
                    product.set_quantity(product.get_quantity() - purchase.get_quantity())
                    productsDict[product.get_productID()] = product
                    p['products'] = productsDict
        s['cartlist'] = []
        s["cart"] = []
        s.close()

        # zh adding points - Start

        # session
        totalsalesrevenue = sum(subtotal)
        try:

            userDict1 = {}
            udb = shelve.open('user.db', 'w')
            userDict1 = udb['Users']
            currentUser = userDict1.get(session.get('loginUser'))
            # add reward points                                 #change the 100 to ur variable total sales for that customer, don: i have changed
            RewardsClass.Reward.plus_points(RewardsClass.Reward, totalsalesrevenue, currentUser)

            # extend expiry date
            RewardsClass.Reward.extend_points_expiry_date(RewardsClass.Reward, currentUser)

            userDict1[session.get('loginUser')] = currentUser
            udb['Users'] = userDict1
        except:
            print('No Reward point added')

        # zh adding points - End

    return render_template('confirmation.html', sale=sale, purchaseList=purchaseList, subtotal=subtotal,
                           count=len(purchaseList), today=today)


@app.route('/forgotpassword')
def forgotpass():
    return render_template('forgotpassword.html')


@app.route('/passconfirm')
def passconfirm():
    return render_template('checkemail.html')


@app.route('/useraccount')
def useraccount():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * From accounts WHERE id = %s',(session['loginid'],))
        user = cursor.fetchone()
        print(user)

        return render_template('useraccount.html', user=user)
    return redirect(url_for('login'))


@app.route('/pastpurchases')
def pastpurchases():
    return render_template('pastpurchases.html')


@app.route('/tracking')
def tracking():
    return render_template('tracking.html')


@app.route('/rewards')  # user rewards
def rewards():
    # session
    userDict1 = {}
    udb = shelve.open('user.db', 'w')
    userDict1 = udb['Users']
    currentUser = userDict1.get(session.get('loginUser'))

    print(userDict1, 'dict')

    RewardsDict = {}
    db = shelve.open('RewardStorage.db', 'c')
    try:
        RewardsDict = db['Rewards']
    except:
        print("error retreiving items from Db['rewards']")

    RewardsList = []

    """
    # test to add points - PLEASE REMOVE

    RewardsClass.Reward.plus_points(RewardsClass.Reward, 100, currentUser)
    currentUser.set_points(currentUser.get_points() + 50)


    # extend expiry date
    #RewardsClass.Reward.extend_points_expiry_date(RewardsClass.Reward, currentUser)

    userDict1[session.get('loginUser')] = currentUser
    udb['Users'] = userDict1
    print(currentUser.get_points(),"rsummary points")
    """

    # upgrading user if they hit 1000 points
    if currentUser.get_membertype() == 'N':
        if currentUser.get_points() >= 1000:
            currentUser.set_membertype('P')

    # check if points expired
    if currentUser.get_points() != 0:
        split_point_expiry_date = currentUser.get_point_expiry_date().split('-')
        e_day = int(split_point_expiry_date[0])
        e_month = int(split_point_expiry_date[1])
        e_year = int(split_point_expiry_date[2])
        e_date = date(e_year, e_month, e_day)

        current_date = date.today()

        if current_date > e_date:
            currentUser.set_points(0)
            # reset cart
            # resting cart after checkout
            All_RewardsCart = db['RewardsCart']
            All_RewardsCart[currentUser.get_userID()] = {}
            db['RewardsCart'] = All_RewardsCart
            # resting cart after checkout - end
            # reset car - end
            flash(Markup(render_template('/includes/PointsExpired.html', currentUser=currentUser)))

    userDict1[session.get('loginUser')] = currentUser
    udb['Users'] = userDict1

    # points expiry check - end

    # displaying rewards
    def by_points(r):
        return r.get_cost(currentUser)

    for key in RewardsDict:
        Reward = RewardsDict.get(key)

        RewardsList.append(Reward)

    # displaying rewards - end

    # quantity select start
    selectQuantity = quantityForm(request.form)
    # quantity select end

    # Rewards transaction history - start
    all_Transactions = {}
    try:
        all_Transactions = db['TransactionHistory']
    except:
        print("all_Transactions = db['TransactionHistory'] error")

    unique_user_transaction = all_Transactions.get(currentUser.get_userID())
    if unique_user_transaction == None:
        unique_user_transaction = {}

    displayList = []
    for key in unique_user_transaction:
        single_transaction = unique_user_transaction.get(key)
        displayList.insert(0, single_transaction)
    print(displayList)
    print(unique_user_transaction, 'h')
    # Transaction history - end

    # for diplaying message of zero items
    RewardsList_Len = len(RewardsList)
    displayList_Len = len(displayList)

    # rewards cart number of items
    All_rewards_cart = {}
    try:
        All_rewards_cart = db['RewardsCart']
    except:
        print("rewards_cart = db['RewardsCart'] error")

    Rewards_cart = All_rewards_cart.get(currentUser.get_userID())
    if Rewards_cart == None:
        Rewards_cart = {}
    number_of_items = 0
    for key in Rewards_cart:
        number_of_items += int(Rewards_cart.get(key))

    db.close()
    udb.close()
    return render_template('userRewards.html', RewardsList=sorted(RewardsList, key=by_points), form=selectQuantity,
                           displayList=displayList, currentUser=currentUser, RewardsList_Len=RewardsList_Len,
                           displayList_Len=displayList_Len, number_of_items_in_cart=number_of_items)


@app.route('/InvalidateReward/<id>', methods=['POST'])
def Invalidate_Reward(id):  # mine #invalidating reward
    RewardsDict = {}
    invalid_rewards = {}
    db = shelve.open('RewardStorage.db', 'w')
    try:
        RewardsDict = db['Rewards']
    except:
        print("invalidate reward() , RewardsDict = db['Rewards'] error ")

    try:
        invalid_rewards = db['Invalid_Rewards']
    except:
        print("invalid rewards dict error")

    # moving to invalid rewards
    invalid_rewards[id] = RewardsDict.get(id)
    # put data back into shelve
    db['Invalid_Rewards'] = invalid_rewards

    # removing item from valid rewards
    image = RewardsDict.get(id).get_image()
    print(image)
    # os.remove(os.path.join(app.config['IMAGE_UPLOADS'], image))
    RewardsDict.pop(id)
    db['Rewards'] = RewardsDict

    # removing from cart
    All_RewardsCart = {}
    try:
        All_RewardsCart = db['RewardsCart']
    except:
        print("delete reward() , RewardsCart = db['RewardsCart'] ")

    for key in All_RewardsCart:
        RewardsCart = All_RewardsCart.get(key)
        if id in RewardsCart:
            RewardsCart.pop(id)

    db['RewardsCart'] = All_RewardsCart

    db.close()
    return redirect(url_for('staffrewards'))


@app.route('/addRewardsCart/<name>', methods=['POST', 'GET'])
def addRewardsCart(name):  # mine
    # session
    userDict1 = {}
    udb = shelve.open('user.db', 'w')
    userDict1 = udb['Users']
    currentUser = userDict1.get(session.get('loginUser'))
    All_RewardsCart = {}

    selectQuantity = quantityForm(request.form)
    RewardsDict = {}

    total_cost = 0  # initialize total_cost
    db = shelve.open('RewardStorage.db', 'w')
    try:
        All_RewardsCart = db['RewardsCart']

    except:
        print("retrieving from shelf error")
    try:
        RewardsDict = db['Rewards']
    except:
        print('line 2014')
    quantity = selectQuantity.quantity.data

    Reward = RewardsDict.get(name)

    RewardsCart = All_RewardsCart.get(currentUser.get_userID())
    if RewardsCart == None:
        RewardsCart = {}

    if request.method == 'POST':

        # calculating total points in cart
        for key in RewardsDict:
            if RewardsCart.get(key, 'Not Found') != 'Not Found':
                total_cost += RewardsDict.get(key).get_cost(currentUser) * RewardsCart.get(key)
        # calculating total points in cart - end

        # checking if insufficent points when adding to cart - user reawards page
        if request.referrer == 'http://127.0.0.1:5000/rewards':
            potential_total = (Reward.get_cost(currentUser) * int(quantity)) + total_cost
            print(total_cost)
            print(quantity)
            print(potential_total, 'poten total')
            if potential_total > currentUser.get_points():
                flash(Markup(render_template('/includes/InsufficientPoints.html')))
                if request.referrer == 'http://127.0.0.1:5000/RewardsSummary':
                    return redirect(url_for('RewardsSummary'))
                else:
                    return redirect(url_for('rewards'))

        # edit quantity check
        if request.referrer == 'http://127.0.0.1:5000/RewardsSummary':
            if int(quantity) >= RewardsCart[Reward.get_name()]:
                difference_quantity = int(quantity) - RewardsCart[Reward.get_name()]
                difference_total = difference_quantity * Reward.get_cost(currentUser)
                to_be_total = total_cost + difference_total
                if to_be_total > currentUser.get_points():
                    flash(Markup(render_template('/includes/InsufficientPoints.html')))
                    return redirect(url_for('RewardsSummary'))

        if Reward.get_name() in RewardsCart and request.referrer == 'http://127.0.0.1:5000/rewards':
            RewardsCart[Reward.get_name()] += int(quantity)
        else:
            print(Reward.get_name(), 'added to cart')
            RewardsCart[Reward.get_name()] = int(quantity)

        All_RewardsCart[currentUser.get_userID()] = RewardsCart
        db['RewardsCart'] = All_RewardsCart
        print(All_RewardsCart)
        print(RewardsCart, 'this is cart')

        db.close()

        if request.referrer == 'http://127.0.0.1:5000/RewardsSummary':
            return redirect(url_for('RewardsSummary'))
        else:
            flash(Markup(render_template('/includes/prompt.html')))
            return redirect(url_for('rewards'))


@app.route('/RewardsSummary')  # mine
def RewardsSummary():
    # session
    userDict1 = {}
    udb = shelve.open('user.db', 'w')
    userDict1 = udb['Users']
    currentUser = userDict1.get(session.get('loginUser'))

    RewardsDict = {}
    DisplayList = []
    All_RewardsCart = {}
    db = shelve.open('RewardStorage.db', 'r')
    try:
        RewardsDict = db['Rewards']
    except:
        print("line 485 shelve retrieving error")
    try:
        All_RewardsCart = db['RewardsCart']
    except:
        print("line 489 retrieving from shelve error")

    RewardsCart = All_RewardsCart.get(currentUser.get_userID())
    if RewardsCart == None:
        RewardsCart = {}

    total_cost = 0
    for key in RewardsDict:
        if RewardsCart.get(key, 'Not Found') != 'Not Found':
            Reward = RewardsDict.get(key)
            DisplayList.append(Reward)
            total_cost += Reward.get_cost(currentUser) * RewardsCart.get(key)

    # form
    selectQuantity = quantityForm(request.form)
    # form - end
    Length = len(DisplayList)
    db.close()
    return render_template('RewardsSummary.html', DisplayList=DisplayList, RewardsCart=RewardsCart, form=selectQuantity,
                           Length=Length, total_cost=total_cost, currentUser=currentUser)


@app.route('/createTransactionHistory', methods=['POST', 'GET'])
def createTransactionHistory():  # mine
    # session
    userDict1 = {}
    udb = shelve.open('user.db', 'w')
    userDict1 = udb['Users']
    currentUser = userDict1.get(session.get('loginUser'))

    db = shelve.open('RewardStorage.db', 'c')
    RewardsCart = {}
    try:
        All_RewardsCart = db['RewardsCart']
    except:
        print("line 525 retreiving from shelve error")
    RewardsDict = {}

    try:
        RewardsDict = db['Rewards']
    except:
        print('Error retrieving Rewards from RewardsDict ')

    # getting date
    dt = date.today()
    Date = str("{0:0=2d}".format(dt.day)) + "-" + str("{0:0=2d}".format(dt.month)) + "-" + str(dt.year)
    all_Transactions = {}
    try:
        all_Transactions = db['TransactionHistory']
    except:
        print('error retrieving transaction history')

    # RTH = REWARD TRANSACTION HISTORY
    user_unqiue_RTH = all_Transactions.get(currentUser.get_userID())
    if user_unqiue_RTH == None:  # for like if all_transactions is empty
        user_unqiue_RTH = {}

    # defining user rewards cart
    RewardsCart = All_RewardsCart.get(currentUser.get_userID())

    # getting total cost
    total_cost = 0
    for key in RewardsDict:
        if RewardsCart.get(key, 'Not Found') != 'Not Found':
            Reward = RewardsDict.get(key)
            total_cost += Reward.get_cost(currentUser) * RewardsCart.get(key)

    # ensure no overlap of keys in RTH
    Number = 1
    Unique_Id = Date + str(Number)
    while True:
        if user_unqiue_RTH.get(Unique_Id, 'Not Found') != "Not Found":
            Number += 1
            Unique_Id = Date + str(Number)
        elif user_unqiue_RTH.get(Unique_Id, 'Not Found') == "Not Found":
            break

    RTH = RewardsTransaction(Date, total_cost, Unique_Id, RewardsCart)

    user_unqiue_RTH[RTH.get_id()] = RTH
    all_Transactions[currentUser.get_userID()] = user_unqiue_RTH
    print(all_Transactions, 'all t')
    db['TransactionHistory'] = all_Transactions

    # minus the point after checkout
    new_user_point = currentUser.get_points() - total_cost
    currentUser.set_points(new_user_point)
    userDict1[session.get('loginUser')] = currentUser
    udb['Users'] = userDict1

    # resting cart after checkout
    All_RewardsCart = db['RewardsCart']
    All_RewardsCart[currentUser.get_userID()] = {}
    db['RewardsCart'] = All_RewardsCart
    # resting cart after checkout - end
    db.close()
    return redirect(url_for('SuccessfulCheckout'))


@app.route('/RemovefromCart/<item>', methods=['POST'])  # mine
def RemovefromCart(item):
    # session
    userDict1 = {}
    udb = shelve.open('user.db', 'w')
    userDict1 = udb['Users']
    currentUser = userDict1.get(session.get('loginUser'))

    db = shelve.open('RewardStorage.db', 'w')
    try:
        All_RewardsCart = db['RewardsCart']
    except:
        print("line 599 retrieving from shelve error")
    RewardsCart = All_RewardsCart.get(currentUser.get_userID())
    RewardsCart.pop(item)
    db['RewardsCart'] = All_RewardsCart
    return redirect(url_for('RewardsSummary'))


@app.route('/EditReward/<name>', methods=['GET', 'POST'])  # mine
def EditReward(name):
    userDict1 = {}
    udb = shelve.open('user.db', 'r')
    userDict1 = udb['Users']
    activeuser = userDict1.get(session.get('loginUser'))

    createRewards = RewardsForm(request.form)
    if request.method == 'POST' and createRewards.validate():
        RewardsDict = {}
        db = shelve.open('RewardStorage.db', 'w')

        try:
            RewardsDict = db['Rewards']
        except:
            print('Error retrieving Rewards')

        Reward = RewardsDict.get(name)

        # upload img
        image_name = RewardsDict.get(name).get_image()
        if request.files:
            if request.files["image"].filename == '':
                image_name = RewardsDict.get(name).get_image()


            else:
                image = request.files["image"]
                if os.path.exists('static/img/RewardsPicUploads/' + image.filename):
                    flash('*Image name is currently used by another reward , please choose another image')
                    return redirect(url_for('EditReward', name=name))

                image_name = RewardsDict.get(name).get_image()
                os.remove(os.path.join(app.config['IMAGE_UPLOADS'], image_name))

                image_name = image.filename
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image_name))

        # upload img - end
        Reward.set_name(createRewards.Reward_Name.data)
        Reward.set_cost(createRewards.Reward_Cost.data)
        Reward.set_Desc(createRewards.Reward_Desc.data)
        Reward.set_image(image_name)
        if createRewards.Reward_Name.data != name:
            RewardsDict[createRewards.Reward_Name.data] = RewardsDict[name]
            del RewardsDict[name]
        db['Rewards'] = RewardsDict

        db.close()

        return redirect(url_for('staffrewards'))


    else:
        RewardsDict = {}
        db = shelve.open('RewardStorage.db', 'c')
        try:
            RewardsDict = db['Rewards']
        except:
            print('Error retrieving Rewards')

        print(name)
        Reward = RewardsDict.get(name)
        createRewards = RewardsForm(request.form)
        createRewards.Reward_Name.data = Reward.get_name()
        createRewards.Reward_Cost.data = Reward.get_cost('Staff')
        createRewards.Reward_Desc.data = Reward.get_Desc()
        image_name = Reward.get_image()

        db.close()

        return render_template('/staff/EditReward.html', form=createRewards, image=image_name, activeuser=activeuser)


@app.route('/SuccessfulCheckout')
def SuccessfulCheckout():
    return render_template('SuccessfulCheckout.html')


@app.route('/Revalidate/<name>', methods=['GET', 'POST'])
def Re_validate(name):
    RewardsDict = {}
    invalid_rewards = {}
    db = shelve.open('RewardStorage.db', 'w')
    try:
        RewardsDict = db['Rewards']
    except:
        print("re-validate reward() , RewardsDict = db['Rewards'] error ")
    try:
        invalid_rewards = db['Invalid_Rewards']
    except:
        print("invalid rewards dict error @ re-validate")

    # xfer items back into rewards db
    RewardsDict[name] = invalid_rewards.get(name)
    db['Rewards'] = RewardsDict
    invalid_rewards.pop(name)
    db['Invalid_Rewards'] = invalid_rewards

    return redirect(url_for('staffrewards'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    error = None
    createUserForm = CreateUserForm(request.form)
    if createUserForm.password.data == createUserForm.passwordRepeat.data:
        if request.method == 'POST' and createUserForm.validate():
            usersDict = {}
            db = shelve.open('user.db', 'c')

            try:
                usersDict = db['Users']
            except:
                print("Error in retrieving Users from user.db")

            user = User.User(createUserForm.firstName.data,
                             createUserForm.lastName.data,
                             createUserForm.gender.data,
                             createUserForm.password.data,
                             createUserForm.email.data,
                             createUserForm.phone.data,
                             createUserForm.city.data,
                             createUserForm.address.data,
                             createUserForm.unit.data,
                             createUserForm.postal.data,
                             date=date.today())

            usersDict[user.get_userID()] = user
            db['Users'] = usersDict
            date.today()
            print(user.get_firstName(), user.get_lastName(),
                  "was stored in shelve successfully with userID =",
                  user.get_userID())

            db.close()
            return redirect(url_for('home'))
    else:
        error = 'Password do not match'
    return render_template('createUser.html', form=createUserForm, error=error)


@app.route('/login', methods=['GET', "POST"])
def login():

    session.clear()
    error = None
    loginform = LoginForm(request.form)

    if request.method == 'POST' and loginform.validate():
        email = loginform.email.data
        password = loginform.password.data

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            if account['type'] == 'Admin' or account['type']=='Staff':
                session['loginid'] = account['id']
                session['email'] = account['email']
                return redirect(url_for('staffhome'))
            else:
                session['loginid'] = account['id']
                session['email'] = account['email']
                return redirect(url_for('useraccount'))
        else:
            error = 'Invalid login credentials'

        '''

        usersList = []
        for key in usersDict:
            user = usersDict.get(key)
            print(user)
            if loginform.email.data == user.get_email() and loginform.password.data == user.get_password():
                if user.get_accounttype() == 'User':
                    session['loginUser'] = user.get_userID()
                    return redirect(url_for('useraccount', id=user.get_userID()))

                elif user.get_accounttype() == 'Admin' or 'Staff':
                    session['loginUser'] = user.get_userID()
                    return redirect(url_for('staffhome'))
            else:
                error = 'Invalid login credentials'
        '''
    else:
        if loginform.recaptcha.errors:
            loginform.recaptcha.errors.pop()
            loginform.recaptcha.errors.append('Captcha Invalid')
    return render_template('login.html', form=loginform, error=error)


@app.route("/accountcreated")
def accountcreated():
    return render_template("accountcreated.html")


@app.route('/retrieveUsers')
def retrieveUsers():
    usersDict = {}
    db = shelve.open('storage.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)
    return render_template('retrieveUsers.html',
                           usersList=usersList, count=len(usersList))


if __name__ == '__main__':
    app.run()
