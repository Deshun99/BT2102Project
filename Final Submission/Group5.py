import mysql.connector
import datetime
import sys
import re
import collections
import pymongo
import pandas as pd
import pprint
from pymongo import MongoClient
# from datetime import datetime
import datetime
import time
from tabulate import tabulate

myclient = MongoClient("mongodb://127.0.0.1:27017/")

mydb_Business = myclient["Business"]
myItems_col = mydb_Business["items"]
myProducts_col = mydb_Business["products"]

mysqldb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    db='testing')
mycursor = mysqldb.cursor()


# --- Customer ---
Customer1 = ('test1', 'rilwan', 'M', 'rilwan@gmail.com', '81234567', 'Pulau Tekong Camp', '12345678')
Customer2 = ('test2', 'jess', 'M', 'jess@gmail.com', '82134567' , 'Sungei Gudong Camp', '12345678')
Customer3 = ('test3', 'deshun', 'M', 'deshun@gmail.com', '91234567', 'Changi Prison', '12345678')
Customer4 = ('test4', 'junding', 'M', 'junding@gmail.com', '92345678', 'Maju Camp', '12345678')
Customer5 = ('test5', 'david', 'M', 'david@gmail.com', '93456789', 'Pasir Laba Camp', '12345678')
Customer6 = ('test6', 'larvine', 'M', 'larvine@gmail.com', '98765432', 'Hendon Camp', '12345678')

listOfCustomer = [Customer1, Customer2, Customer3, Customer4, Customer5, Customer6]

# --- Administrator ---
Admin1 = ('admin1', 'tan eng chye', 'M', '92345678', 'Inevitable')
Admin2 = ('admin2', 'joseph issac schooling', 'M', '98762345', 'IloveNS123')
Admin3 = ('admin3', 'Quah Zheng Wen', 'M', '87650987', 'IloveNS234')
Admin4 = ('admin4', 'Soh Rui Yong', 'M', '98675432', '6min53sec')
Admin5 = ('admin5', 'Yugi Moto', 'M', '98654337', 'itsTimeToDuel')

listOfAdmin = [Admin1, Admin2, Admin3, Admin4, Admin5]

# List of tuples containing the admin users name and password
def addCustomer(listOfTuples):
    strg = ""
    count = 0
    for tup in listOfTuples:
        customerID, name, gender, email, phoneNumber, address, password = tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]
        newTup = (customerID,) + (name,) + (gender,) + (email,) + (phoneNumber,) + (address,) + (password,)
        if count == len(listOfTuples) - 1:
            strg += str(newTup)
        else:
            strg += str(newTup) + ", "
        count += 1
    return strg

#
def creatingCustomer(listOfTuples):
    try:
        mycursor.execute(
            "INSERT into customer VALUES " + addCustomer(listOfTuples))
        mysqldb.commit()
        print('Records inserted successfully!')
    except:
        mysqldb.rollback()
        mysqldb.close()

def displayCustomerRecords():
    try:
        mycursor.execute("SELECT * from customer")
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Customer ID", "name", "gender", "email address", "phone number", "address", "password"]))
    except:
        print('Error: Unable to fetch data.')
        mysqldb.close()

# displayCustomerRecords()

def retrieveCustomerID(username):
    mycursor.execute(
        f"SELECT * FROM customer WHERE CustomerID = '{username}'")
    cursor = mycursor.fetchall()
    return cursor[0][0]

# retrieveCustomerID('test1')


def emptyCursor(mycursor):
    return len(mycursor.fetchall()) == 0


def addAdmin(listOfTuples):
    strg = ""
    count = 0
    for tup in listOfTuples:
        administratorID, name, gender, phoneNumber, password = tup[0], tup[1], tup[2], tup[3], tup[4]
        newTup = (administratorID,) + (name,) + (gender,) + (phoneNumber,) + (password,)
        if count == len(listOfTuples) - 1:
            strg += str(newTup)
        else:
            strg += str(newTup) + ", "
        count += 1
    return strg


def creatingAdmin(listOfTuples):
    try:
        mycursor.execute(
            "INSERT into admin VALUES " + addAdmin(listOfTuples))
        mysqldb.commit()
        print('Records inserted successfully!')
    except:
        mysqldb.rollback()
        mysqldb.close()

def displayAdminRecords():
    try:
        mycursor.execute("SELECT * from admin")
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Administrator ID", "name", "gender", "phone number", "password"]))
    except:
        print('Error: Unable to fetch data.')
        mysqldb.close()

# displayAdminRecords()



################################## Basic Product Search Function ###########################################################
def basicProductSearchByCategory(category):
    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM products WHERE Category = '{category}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        if len(list(result)) > 0:
            print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
            print("\n")
            listOfProd = list(result)
            option = input("Do you want to search the individual items (Y/N) ? ")
            if option == 'Y':
                print("There are a total of " + str(len(result)) + " products to select your item")
                selection = input("Select your option: ")
                print("Searching for products...\n")
                listOfItemAvailable(listOfProd, int(selection) - 1)
        else :
            print("Invalid search\n")
    except:
        mysqldb.rollback()
        mysqldb.close()

def listOfItemAvailable(keyword, index):
    try:
        query = f"SELECT ItemID, Category, Color, Factory, PowerSupply, Model, ProductionYear " \
                f"FROM items s WHERE s.Category = '{keyword[index][0]}' AND s.Model = '{keyword[index][1]}' " \
                f"AND s.PurchaseStatus = 'Unsold'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["ItemID", "Category", "Color", "Factory", "PowerSupply",
                                        "Model", "Production Year"]))
        print("\n")
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()

def basicProductSearchByModel(model):
    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM products WHERE Model = '{model}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        if len(list(result)) > 0:
            print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
            print("\n")
            listOfProd = list(result)
            option = input("Do you want to search the individual items (Y/N) ? ")
            if option == 'Y':
                print("There are a total of " + str(len(result)) + " products to select your item")
                selection = input("Select your option: ")
                print("Searching for products...\n")
                listOfItemAvailable(listOfProd, int(selection) - 1)
        else :
            print("Invalid search\n")
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()


def basicProductFilterByPrice(price):

    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM products WHERE Price <= {price}"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
        print('\n')
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()


def basicProductFilterByColor(color):

    try:
        query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM items s WHERE " \
                f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
                f"AND s.Color = '{color}') FROM products p"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
        print("\n")
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()

def basicProductFilterByFactory(factory):

    try:
        query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM items s WHERE " \
                f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
                f"AND s.Factory = '{factory}') FROM products p"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
    except:
        mysqldb.rollback()
        mysqldb.close()


def basicProductFilterByProductionYear(productionYear):
    try:
        query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM items s WHERE " \
                f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
                f"AND s.ProductionYear = '{productionYear}') FROM products p"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["Product Category", "Model", "Price", "Warranty", "Inventory"]))
    except:
        mysqldb.rollback()
        mysqldb.close()

#####################################################################################################################
# basicProductSearchByCategory('Lights')
# basicProductFilterByFactory('Malaysia')
# basicProductFilterByProductionYear('2019')



# Checking inventory stocks for each products
# def inventoryStock(category, model):
#     product = 0
#     try:
#         query = f"SELECT ProductID FROM products WHERE Category = '{category}' AND Model = '{model}'"
#         mycursor.execute(query)
#         results = mycursor.fetchone()
#         product = results[0]
#     except:
#         mysqldb.rollback()
#         mysqldb.close()
#
#     try:
#         query = f"SELECT COUNT(ItemID) FROM items WHERE Category = '{category}' AND Model = '{model}' " \
#                 f"AND PurchaseStatus = 'UNSOLD'"
#         mycursor.execute(query)
#         result = mycursor.fetchone()
#         print("Product " + str(product) + " currently has " + str(result[0]) + " items in stock")
#     except:
#         mysqldb.rollback()
#         mysqldb.close()


# Searching Item based on Category
def searchByCategory(category):
    myquery = {"Category": category, "PurchaseStatus": "Unsold"}
    return myItems_col.find(myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})


# Searching Item based on Model
def searchByModel(model):
    myquery = {"Model": model, "PurchaseStatus": "Unsold"}
    return myItems_col.find(myquery, {"_id": 0, "ServiceStatus": 0})


# Searching based on ItemID
def simpleSearch(id):
    return myItems_col.find({"ItemID": id}, {"_id": 0, "ServiceStatus": 0})

# Calculating the inventory Stocks
def inventoryStocks(category, model):
    return myItems_col.count_documents({"Category": category, "Model": model, "PurchaseStatus": "Unsold"})

# Search based on Product Category
def simpleSearchProductCategory(category):
    myquery = {"Category": category}
    result = list(myProducts_col.find(myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))

    dataFrame = pd.DataFrame(result)
    print(dataFrame)
    # for x in myProducts_col.find(myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}):
    #      print(x)
    #      print("Inventory stocks: " + str(inventoryStocks(x["Category"], x["Model"])))

# Search based on Model
def simpleSearchModel(model):
    myquery = {"Model": model}
    for x in myProducts_col.find(myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}):
        print(x)
        print("Inventory stocks: " + str(inventoryStocks(x["Category"], x["Model"])))

# Import the item dataset from MongoDB to MySQL
def ItemImports():
    lst_importable = []
    cursor = myItems_col.find({}, {"ItemID": 1, "Category": 1, "Color": 1, "Factory": 1, "PowerSupply": 1,
                                   "PurchaseStatus": 1, "ProductionYear": 1, "Model": 1, "ServiceStatus": 1})
    for cur in cursor:
        try:
            data = (cur['ItemID'], cur['Category'], cur['Color'], cur['Factory'],
                    cur['PowerSupply'], cur['PurchaseStatus'], cur['ProductionYear'], cur['Model'],
                    cur['ServiceStatus'])
            lst_importable.append(data)
        except:
            continue
    query = '''INSERT INTO testing.items(ItemID, Category, Color, Factory, PowerSupply, PurchaseStatus, ProductionYear, 
    Model, ServiceStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    mycursor.executemany(query, lst_importable)
    mysqldb.commit()
    print("Successfully imported " + str(len(lst_importable)) + " books!")
    mysqldb.close()

# Import the product dataset from MongoDB to MySQL
def ProductImports():
    lst_importable = []
    cursor = myProducts_col.find({}, {"Category": 1, "Cost ($)": 1, "Model": 1, "Price ($)": 1, "ProductID": 1,
                                      "Warranty (months)": 1})
    for cur in cursor:
        try:
            data = (str(cur['ProductID']), cur['Category'], str(cur['Cost ($)']), cur['Model'],
                    str(cur['Price ($)']), str(cur['Warranty (months)']),
                    str(inventoryStocks(cur["Category"], cur["Model"])))
            lst_importable.append(data)
        except:
            continue
    print(lst_importable)
    query = '''INSERT INTO testing.products(ProductID, Category, Cost, Model, Price,
    Warranty, Inventory) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    mycursor.executemany(query, lst_importable)
    mysqldb.commit()
    print("Successfully imported " + str(len(lst_importable)) + " products!")
    mysqldb.close()

# Prints out the Product List
def printProduct():
    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM testing.products"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
    except:
        mysqldb.rollback()
        mysqldb.close()

# # Perform Simple Search based on ProductID
# def simpleSearch(id):
#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM testing.products WHERE ProductID = '{str(id)}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         print(tabulate(result, headers=["Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
#     except:
#         mysqldb.rollback()
#         mysqldb.close()
#
# # Perform Simple Search based on Model
# def simpleSearchModel(model):
#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM testing.products WHERE Model = '{model}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         print(tabulate(result, headers=["Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
#     except:
#         mysqldb.rollback()
#         mysqldb.close()
#
# # Perform Simple Search based on Category
# def simpleSearchCategory(category):
#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM testing.products WHERE Category = '{category}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         print(tabulate(result, headers=["Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
#     except:
#         mysqldb.rollback()
#         mysqldb.close()
#


# printProduct()


# searchByCategory("Lights")
# simpleSearchProductCategory("Lights")

# specificProduct("Lights", "Light1")
# specificProduct('Lights', 'Light2')
# specificProduct('Lights', 'SmartHome1')
# specificProduct('Locks', 'Safe1')
# specificProduct('Locks', 'Safe2')
# specificProduct('Locks', 'Safe3')
# specificProduct('Locks', 'SmartHome1')
# inventoryStock('Lights', 'Light2')
#
def purchaseItem(username):
    # Tables
    booksTable = "Library.Book"
    booksBorrowedTable = "Library.Borrow"
    booksReservedTable = "Library.Reserve"
    customerTable = "testing.customer"
    # Messages
    notRegisteredMsg = "You are not registered!"
    alreadyReservedMsg = "You have already reserved this book!"
    alreadyBorrowedMsg = "You have already borrowed this book!"
    bookReservedMsg = "Book was already reserved!"
    reservedSuccessMsg = "You have succesfully reserved the book"
    borrowedSuccessMsg = "Book was succesfully borrowed!"
    maxBookMsg = "Maximum number of books reached!!!!"
    existingFinesMsg = "You got existing fines, so you cannot borrow any books!"

    # Datetime values
    # timing = datetime.datetime.now()
    # print(timing)

    # duedate = extendingDateTime(timing)

    print("Hi chibao")
    try:
        mycursor.execute(
            f"SELECT * FROM customer WHERE CustomerID LIKE '{username}'")
        if emptyCursor(mycursor):
            print(notRegisteredMsg)
        else:

            # id = retrieveCustomerID(username)
            # if reachMaxLoan(id):
            #     print(maxBookMsg)
            # elif gotFines(id):
            #     print(existingFinesMsg)
            # else:

            while True :
                print("Basic Product Search by:")
                print("1. Product Category")
                print("2. Models")
                print("3. Filter by price")
                print("4. Filter by Color")
                print("5. Filter by Factory")
                print("6. Filter by Production Year")
                print("7. Exit\n")

                option = input("Your selection: ")
                if option == '1':
                    prodCat = input("Enter a Product Category: ")
                    print("Searching based on Product Category...")
                    basicProductSearchByCategory(prodCat)
                elif option == '2':
                    model = input("Enter a Model: ")
                    print("Searching based on Model...")
                    basicProductSearchByModel(model)
                elif option == '3':
                    filterPrice = input("Enter a price (upperbound): ")
                    print("Searching based on Price (upperbound)...")
                    basicProductFilterByPrice(filterPrice)
                elif option == '4':
                    filterColor = input("Enter a color: ")
                    print("Searching based on Color...")
                    basicProductFilterByColor(filterColor)
                elif option == '5':
                    filterFactory = input("Enter a Factory: ")
                    print("Searching based on Factory...")
                    basicProductFilterByFactory(filterFactory)
                elif option == '6':
                    filterProductYear = input("Enter a Production Year: ")
                    print("Searching based on Production Year...")
                    basicProductFilterByProductionYear(filterProductYear)
                elif option == '7':
                    break
    except:
        print("There is an error in your selection!")
        mysqldb.rollback()
        mysqldb.close()


purchaseItem('test1')