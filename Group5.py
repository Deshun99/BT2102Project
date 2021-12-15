import mysql.connector
import datetime
import sys
import re
import collections
import pymongo
import pandas as pd
import pprint

from mysqlx.protobuf.mysqlx_resultset_pb2 import DATE
from pymongo import MongoClient
# from datetime import datetime
import datetime
import time
from tabulate import tabulate
from dateutil.relativedelta import relativedelta

myclient = MongoClient("mongodb://127.0.0.1:27017/")

mydb_Business = myclient["Business"]
myItems_col = mydb_Business["items"]
myProducts_col = mydb_Business["products"]

mysqldb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    db='business')

mycursor = mysqldb.cursor()

pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)

# --- Customer ---
Customer1 = ('rilwan', '12345678', 'M', 'rilwan@gmail.com',
             'Pulau Tekong Camp', '81234567')
Customer2 = ('jess', '12345678', 'M', 'jess@gmail.com',
             'Sungei Gudong Camp', '82134567')
Customer3 = ('deshun', '12345678', 'M', 'deshun@gmail.com',
             'Changi Prison', '91234567')
Customer4 = ('junding', '12345678', 'M',
             'junding@gmail.com', 'Maju Camp', '92345678')
Customer5 = ('david', '12345678', 'M', 'david@gmail.com',
             'Pasir Laba Camp', '93456789')
Customer6 = ('larvine', '12345678', 'M',
             'larvine@gmail.com', 'Hendon Camp', '98765432')

listOfCustomer = [Customer1, Customer2,
                  Customer3, Customer4, Customer5, Customer6]

# --- Administrator ---
Admin1 = ('tan eng chye', 'Inevitable', 'M', '92345678')
Admin2 = ('joseph issac schooling', 'IloveNS123', 'M', '98762345')
Admin3 = ('Quah Zheng Wen', 'IloveNS234', 'M', '87650987')
Admin4 = ('Soh Rui Yong', '6min53sec', 'M', '98675432')
Admin5 = ('Yugi Moto', 'itsTimeToDuel', 'M', '98654337')

listOfAdmin = [Admin1, Admin2, Admin3, Admin4, Admin5]

# List of tuples containing the admin users name and password


def addCustomer(listOfTuples):
    strg = ""
    count = 0
    for tup in listOfTuples:
        name, password, gender, email, address, phoneNumber = tup[
            0], tup[1], tup[2], tup[3], tup[4], tup[5]
        newTup = (name,) + (password,) + (gender,) + \
            (email,) + (address,) + (phoneNumber,)
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
            "INSERT into business.customer (CustomerName, CustomerPassword, Gender, EmailAddress, Address, PhoneNumber)"
            " VALUES " + addCustomer(listOfTuples))
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


def emptyCursor(mycursor):
    return len(mycursor.fetchall()) == 0


def addAdmin(listOfTuples):
    strg = ""
    count = 0
    for tup in listOfTuples:
        name, password, gender, phoneNumber = tup[0], tup[1], tup[2], tup[3]
        newTup = (name,) + (password,) + (gender,) + (phoneNumber,)
        if count == len(listOfTuples) - 1:
            strg += str(newTup)
        else:
            strg += str(newTup) + ", "
        count += 1
    return strg


def creatingAdmin(listOfTuples):
    try:
        mycursor.execute(
            "INSERT into business.administrator "
            "(AdministratorName, AdministratorPassword, Gender, PhoneNumber) VALUES " + addAdmin(listOfTuples))
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

################################## Login & Registration Function ###########################################################


def loginCustomer(userID, password):
    notRegistered = "UserID or password is invalid"
    successRegistered = "Login Successfully as a customer"
    try:
        mycursor.execute(
            f"SELECT * FROM business.customer WHERE CustomerID = '{userID}' AND CustomerPassword = '{password}'")
        if emptyCursor(mycursor):
            print(notRegistered)
            return False
        else:
            print(successRegistered)
            return True
    except:
        mysqldb.rollback()
    mysqldb.close()


def registerCustomer(userID, name, password, gender, emailAddress, address, phoneNumber):
    userIDisUsed = "UserID is already taken please select a different UserID"
    successRegistered = "Successfully registered as a customer"
    try:
        mycursor.execute(
            f"SELECT * FROM business.customer WHERE CustomerID = '{userID}'")
        if emptyCursor(mycursor):
            mycursor.execute(f"INSERT INTO business.customer VALUES ('{userID}', '{name}', '{password}', '{gender}',"
                             f"'{emailAddress}', '{address}', '{phoneNumber}')")
            mysqldb.commit()
            print(successRegistered)
            return True
        else:
            print(userIDisUsed)
            return False
    except:
        mysqldb.rollback()
    mysqldb.close()

# registerCustomer("test1", "Najib Razak", "boskku", "M", "1mdb@gmail.com", "Jalan Merdeka", "89678765")


def loginAdministrator(adminID, password):
    notRegistered = "AdministratorID or password is invalid"
    successRegistered = "Login Successfully as a administrator"
    try:
        mycursor.execute(
            f"SELECT * FROM business.administrator WHERE AdministratorID = '{adminID}' AND AdministratorPassword = '{password}'")
        if emptyCursor(mycursor):
            print(notRegistered)
            return False
        else:
            print(successRegistered)
            return True
    except:
        mysqldb.rollback()
    mysqldb.close()


def registerAdministrator(adminID, name, password, gender, phoneNumber):
    userIDisUsed = "AdministratorID is already taken please select a different AdministratorID"
    successRegistered = "Successfully registered as a administrator"
    try:
        mycursor.execute(
            f"SELECT * FROM business.administrator WHERE AdministratorID = '{adminID}'")
        if emptyCursor(mycursor):
            mycursor.execute(f"INSERT INTO business.administrator VALUES ('{adminID}', '{name}', '{password}', '{gender}',"
                             f"'{phoneNumber}')")
            mysqldb.commit()
            print(successRegistered)
            return True
        else:
            print(userIDisUsed)
            return False
    except:
        mysqldb.rollback()
    mysqldb.close()


# registerAdministrator("SRY123", "Daud Ali Aser", "wgtowadio", "M", "81234567")

###################################### MONGOL DB SEARCH FUNCTION ######################################################
# Searching Item based on Category
def searchByCategory(category):
    myquery = {"Category": category, "PurchaseStatus": "Unsold"}
    return myItems_col.find(myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})


# Searching Item based on Model
def searchByModel(model):
    myquery = {"Model": model, "PurchaseStatus": "Unsold"}
    return myItems_col.find(myquery, {"_id": 0, "ServiceStatus": 0})


# Searching based on ItemID #Administrator Function only
def simpleSearchId(id):
    result = list(myItems_col.find(
        {"ItemID": id}, {"_id": 0, "ServiceStatus": 0}))
    dataFrame = pd.DataFrame(result)
    print(dataFrame)


def isAdministrator(username):
    try:
        mycursor.execute(
            f"SELECT * FROM business.administrator WHERE AdministratorID = '{username}'")
        if emptyCursor(mycursor):
            return False
        else:
            return True
    except:
        mysqldb.rollback()
    mysqldb.close()
    return False

# Calculating the inventory Stocks


def inventoryStocks(category, model):
    return myItems_col.count_documents({"Category": category, "Model": model, "PurchaseStatus": "Unsold"})


# Search based on Product Category
def simpleSearchProductCategory(category, username):
    try:
        myquery = {"Category": category}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocks(x["Category"], x["Model"]))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocks(x["Category"], x["Model"]))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByModel(result, selection)
    except:
        print("Invalid Category")


# Searching the item based on model
def searchItemByModel(stuff, selection):
    try:
        model = stuff[selection]["Model"]
        myquery = {"Model": model, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")


# Searching products based on Model
def simpleSearchModel(model, username):
    try:
        myquery = {"Model": model}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocks(x["Category"], x["Model"]))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocks(x["Category"], x["Model"]))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByCategory(result, selection)

    except:
        print("Invalid Model")

# Searching the item based on category


def searchItemByCategory(stuff, selection):
    try:
        category = stuff[selection]["Category"]
        myquery = {"Category": category, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")

# Searching products based on Price


def simpleSearchPrice(price):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        result = list(myProducts_col.find(
            myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
        dataFrame = pd.DataFrame(result)

        listInventory = []
        for x in result:
            listInventory.append(inventoryStocks(x["Category"], x["Model"]))

        dataFrame.insert(4, "Inventory", listInventory, True)
        print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByCategoryModel(result, selection)

    except:
        print("Invalid Price")

# Searching the item based on category Model


def searchItemByCategoryModel(stuff, selection):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category,
                   "Model": model, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")


# Searching products based on Color
def simpleSearchColor(color, username):
    try:
        if(isAdministrator(username)):

            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            print(result)
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndColor(
                    x["Category"], x["Model"], color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:

            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndColor(
                    x["Category"], x["Model"], color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByColor(result, selection, color)
    except:
        print("Invalid search")


# Calculating the inventory Stocks with the color filter
def inventoryStocksAndColor(category, model, color):
    return myItems_col.count_documents({"Category": category, "Model": model, "Color": color, "PurchaseStatus": "Unsold"})

# Searching the item based on category


def searchItemByColor(stuff, selection, color):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model,
                   "Color": color, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")


# Searching products based on Factory
def simpleSearchFactory(factory, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactory(
                    x["Category"], x["Model"], factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactory(
                    x["Category"], x["Model"], factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactory(result, selection, factory)

    except:
        print("Invalid Factory")

# Calculating the inventory Stocks with the factory filter


def inventoryStocksAndFactory(category, model, factory):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "Factory": factory, "PurchaseStatus": "Unsold"})

# Searching the item based on factory filter


def searchItemByFactory(stuff, selection, factory):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model,
                   "Factory": factory, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")

# Searching products based on Production Year


def simpleSearchProdYear(prodYear, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYear(
                    x["Category"], x["Model"], prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYear(
                    x["Category"], x["Model"], prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYear(result, selection, prodYear)

    except:
        print("Invalid Production Year")


# Calculating the inventory Stocks with the factory filter
def inventoryStocksAndProdYear(category, model, prodYear):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "ProductionYear": str(prodYear), "PurchaseStatus": "Unsold"})

# Searching the item based on factory filter


def searchItemByProdYear(stuff, selection, prodYear):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model,
                   "ProductionYear": prodYear, "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")

######################## MongoDB 2 Filter for Search Function ###########################################################

# Searching products based on Production Year And Factory


def simpleSearchProdYearFactory(prodYear, factory, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearFactory(
                    x["Category"], x["Model"], prodYear, factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearFactory(
                    x["Category"], x["Model"], prodYear, factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYearFactory(result, selection, prodYear, factory)

    except:
        print("Invalid Production Year")

# Calculating the inventory Stocks with the factory and production Year filter


def inventoryStocksAndProdYearFactory(category, model, prodYear, factory):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "ProductionYear": str(prodYear), "PurchaseStatus": "Unsold",
         "Factory": factory})


# Searching the item based on factory and production year filter
def searchItemByProdYearFactory(stuff, selection, prodYear, factory):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model, "ProductionYear": prodYear, "Factory": factory,
                   "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")

# Searching products based on Production Year And Color


def simpleSearchProdYearColor(prodYear, color, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearColor(
                    x["Category"], x["Model"], prodYear, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearColor(
                    x["Category"], x["Model"], prodYear, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYearColor(result, selection, prodYear, color)

    except:
        print("Error in search")


# Calculating the inventory Stocks with the color and production Year filter
def inventoryStocksAndProdYearColor(category, model, prodYear, color):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "PurchaseStatus": "Unsold", "Color": color, "ProductionYear": str(prodYear)})


# Searching the item based on color and production year filter
def searchItemByProdYearColor(stuff, selection, prodYear, color):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model, "ProductionYear": prodYear, "Color": color,
                   "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")


# Searching products based on Production Year And Price
def simpleSearchProdYearPrice(prodYear, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYear(
                    x["Category"], x["Model"], prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYear(
                    x["Category"], x["Model"], prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYear(result, selection, prodYear)

    except:
        print("Error in search")


# Searching products based on Factory And Color
def simpleSearchFactoryColor(factory, color, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColor(
                    x["Category"], x["Model"], factory, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColor(
                    x["Category"], x["Model"], factory, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactoryColor(result, selection, factory, color)

    except:
        print("Error in search")


# Calculating the inventory Stocks with the color and factory filter
def inventoryStocksAndFactoryColor(category, model, factory, color):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "Factory": factory, "PurchaseStatus": "Unsold",
         "Color": color})


# Searching the item based on color and factory filter
def searchItemByFactoryColor(stuff, selection, factory, color):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model, "Factory": factory, "Color": color,
                   "PurchaseStatus": "Unsold"}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")


# Searching products based on Factory And Price
def simpleSearchFactoryPrice(factory, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactory(
                    x["Category"], x["Model"], factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactory(
                    x["Category"], x["Model"], factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactory(result, selection, prodYear)

    except:
        print("Error in search")


# Searching products based on Color And Price
def simpleSearchColorPrice(color, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndColor(
                    x["Category"], x["Model"], color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndColor(
                    x["Category"], x["Model"], color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByColor(result, selection, color)

    except:
        print("Error in search")


####################### MongoDB 3 Filters for Search Function ##########################################################

# Searching products based on Factory, Color And Price
def simpleSearchFactoryColorPrice(factory, color, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColor(
                    x["Category"], x["Model"], factory, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColor(
                    x["Category"], x["Model"], factory, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactoryColor(result, selection, factory, color)
    except:
        print("Error in search")


# Searching products based on Factory, Production Year And Price
def simpleSearchFactoryProductionYearPrice(factory, prodYear, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearFactory(
                    x["Category"], x["Model"], prodYear, factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearFactory(
                    x["Category"], x["Model"], prodYear, factory))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYearFactory(result, selection, prodYear, factory)
    except:
        print("Error in search")


def simpleSearchColorProductionYearPrice(color, prodYear, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearColor(
                    x["Category"], x["Model"], prodYear, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndProdYearColor(
                    x["Category"], x["Model"], prodYear, color))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByProdYearColor(result, selection, prodYear, color)
    except:
        print("Error in search")


def simpleSearchColorProductionYearFactory(color, prodYear, factory, username):
    try:
        if(isAdministrator(username)):
            result = list(myProducts_col.find({}, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColorProdYear(
                    x["Category"], x["Model"], factory, color, prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                {}, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocksAndFactoryColorProdYear(x["Category"], x["Model"], factory, color, prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactoryColorProdYear(
                result, selection, factory, color, prodYear)
    except:
        print("Error in search")


# Calculating the inventory Stocks with the color and factory and production year filter
def inventoryStocksAndFactoryColorProdYear(category, model, factory, color, prodYear):
    return myItems_col.count_documents(
        {"Category": category, "Model": model, "Factory": factory, "PurchaseStatus": "Unsold",
         "Color": color, "ProductionYear": str(prodYear)})


# Searching the item based on color and factory and production year filter
def searchItemByFactoryColorProdYear(stuff, selection, factory, color, prodYear):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category, "Model": model, "Factory": factory, "Color": color,
                   "PurchaseStatus": "Unsold", "ProductionYear": prodYear}
        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option")

####################### MongoDB 4 Filters for Search Function ##########################################################


def simpleSearchAllFilter(color, prodYear, factory, price, username):
    try:
        myquery = {"Price ($)": {'$lte': price}}
        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksAndFactoryColorProdYear(
                    x["Category"], x["Model"], factory, color, prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(
                    inventoryStocksAndFactoryColorProdYear(x["Category"], x["Model"], factory, color, prodYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItemByFactoryColorProdYear(
                result, selection, factory, color, prodYear)
    except:
        print("Error in search")


def getProductID(model, category):
    result = myProducts_col.find({"Model": model, "Category": category})
    listofstuff = list(result)
    return listofstuff[0]['ProductID']


# Import the item dataset from MongoDB to MySQL
def ItemImports():
    lst_importable = []
    cursor = myItems_col.find({}, {"ItemID": 1, "Category": 1, "Color": 1, "Factory": 1, "PowerSupply": 1,
                                   "PurchaseStatus": 1, "ProductionYear": 1, "Model": 1, "ServiceStatus": 1})
    for cur in cursor:
        try:
            data = (cur['ItemID'], cur['PurchaseStatus'], str(
                getProductID(cur['Model'], cur['Category'])))
            lst_importable.append(data)
        except:
            continue
    query = '''INSERT INTO business.items(ItemID, PurchaseStatus, ProductID) VALUES (%s, %s, %s)'''
    mycursor.executemany(query, lst_importable)
    mysqldb.commit()
    print("Successfully imported " + str(len(lst_importable)) + " items!")
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
    query = '''INSERT INTO business.products(ProductID, Category, Cost, Model, Price,
    Warranty, Inventory) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    mycursor.executemany(query, lst_importable)
    mysqldb.commit()
    print("Successfully imported " + str(len(lst_importable)) + " products!")
    mysqldb.close()


# Prints out the Product List
def printProduct():
    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM business.products"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
    except:
        mysqldb.rollback()
        mysqldb.close()


# Prints out the list of items purchased by the customer
def printPurchasedList(username):
    try:
        query = f"SELECT * FROM business.purchased WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if len(list(result)) > 0:
            print(tabulate(result, headers=[
                  "Customer ID", "Item ID", "Purchase Date", "Warranty End Date"]))
            print("\n")
        else:
            return 0
    except:
        mysqldb.rollback()

    mysqldb.close()

# Prints out the list of items under servicing for customer


def printItemServicingList(username):
    try:
        query = f"SELECT * FROM business.servicerequest WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Request ID", "Request Date", "Request Status", "Service Status", "Customer ID", "Item ID"]))
        print("\n")

    except:
        mysqldb.rollback()
    mysqldb.close()

# Prints out the list of items pending for service payment for the customer


def printServiceFee(username):
    try:
        query = f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=["Payment Creation Date", "Payment Settlement Date",
              "Due Date", "Service Fee Amount", "Item ID", "Customer ID"]))
        print("\n")

    except:
        mysqldb.rollback()
    mysqldb.close()

# Obtain the warranty end date when customer purchase the item


def getWarrantyEndDate(date, item):
    try:
        query = f"SELECT p.Warranty FROM items s, products p WHERE s.ItemID = '{item}' AND s.ProductID = p.ProductID "
        mycursor.execute(query)
        result = mycursor.fetchone()
        warranty = int(list(result)[0])
        return date + relativedelta(months=warranty)
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()

# Obtaining the due date for the service payment


def getDueDate(date):
    return date + datetime.timedelta(days=10)

# Obtaining the service fee amount that the customer needs to pay for


def getServiceFeeAmount(item):
    try:
        query = f"SELECT p.Cost FROM items s, products p WHERE s.ItemID = '{item}' AND s.ProductID = p.ProductID "
        mycursor.execute(query)
        result = mycursor.fetchone()
        cost = int(list(result)[0])
        return 40 + (0.2 * cost)
    except:
        print("Error occurred in search\n")
        mysqldb.rollback()
        mysqldb.close()


# This function enable customers to checkout their items
def checkoutItem(username):
    itemNotAvailable = "Item is not available or already sold!"

    timing = datetime.datetime.now()

    successPurchaseItem = "You have successfully purchased the item"

    try:
        itemID = input("Select a ItemID to purchase: ")
        mycursor.execute(
            f"SELECT * FROM business.items WHERE ItemID = '{itemID}' AND PurchaseStatus = 'Unsold'")
        if emptyCursor(mycursor):
            print(itemNotAvailable)
        else:
            sqlQuery = f"INSERT INTO business.purchased " \
                       f"VALUES('{username}', {itemID}, DATE('{timing}'), DATE('{getWarrantyEndDate(timing, itemID)}'))"
            mycursor.execute(sqlQuery)

            updateQuery = f"UPDATE items SET PurchaseStatus = 'Sold' WHERE ItemID = '{item}'"
            mycursor.execute(updateQuery)

            print("Item table is updated successfully!")
            mysqldb.commit()
            print(successPurchaseItem)
    except:
        mysqldb.rollback()
    mysqldb.close()

# This function checks whether the item purchased by customer is still under warranty


def checkWarranty(itemid, time):
    try:
        myquery = f"SELECT WarrantyEndDate FROM business.purchased WHERE ItemID = {itemid}"
        mycursor.execute(myquery)
        result = mycursor.fetchone()
        retrieveDate = list(result)

        if time <= retrieveDate[0]:
            return "Submitted"
        else:
            return "Submitted and Waiting for payment"
    except:
        mysqldb.rollback()
        mysqldb.close()

# This function checks whether the item purchased by customer is still under warranty and updates the service status


def checkServiceStatus(itemid, time):
    try:
        myquery = f"SELECT WarrantyEndDate FROM business.purchased WHERE ItemID = {itemid}"
        mycursor.execute(myquery)
        result = mycursor.fetchone()
        retrieveDate = list(result)

        if time <= retrieveDate[0]:
            return "Waiting for approval"
        else:
            return " "
    except:
        mysqldb.rollback()
        mysqldb.close()


def getRequestID(customer, itemid):
    try:
        myquery = f"SELECT RequestID FROM business.request WHERE ItemID = {itemid} AND CustomerID = '{customer}'" \
                  f"AND RequestStatus"
        mycursor.execute(myquery)
        result = mycursor.fetchone()
        retrieveID = list(result)
        print(retrieveID)

        return int(retrieveID[0])
    except:
        mysqldb.rollback()

    mysqldb.close()


# This function is meant for customers to view their service payment
def viewServiceFee(username):
    noServiceFee = "You do not have any service fee to settle"
    try:
        mycursor.execute(
            f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:
            print(noServiceFee)
        else:
            mycursor.execute(
                f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
            result = mycursor.fetchall()
            print(tabulate(result, headers=[
                  "Payment Creation Date", "Payment Settlement Date", "Due Date", "Service Fee", "Item ID", "Customer ID"]))
            print("\n")
    except:
        mysqldb.rollback()
    mysqldb.close()


def getItemIDFromServiceRequest(request):
    try:
        mycursor.execute(
            f"SELECT ItemID FROM business.request WHERE RequestID = {request}")
        result = list(mycursor.fetchone())
        return result[0]
    except:
        mysqldb.rollback()

    mysqldb.close()


# This function facilitates the customer's request for servicing of their products
def requestForService(username):
    successRequestItem = "You have successfully requested for servicing"
    timing = datetime.datetime.now()

    try:
        itemInput = input("Enter the ItemID that you wish to service: ")

        mycursor.execute(f"SELECT * FROM business.purchased "
                         f"WHERE ItemID = {itemInput}")
        if emptyCursor(mycursor):
            print("Invalid ItemID input")
        else:
            mycursor.execute(f"SELECT * FROM business.request "
                             f"WHERE ItemID = {itemInput}")
            if emptyCursor(mycursor):

                requestStatus = checkWarranty(itemInput, timing)
                serviceStatus = checkServiceStatus(itemInput, timing)

                sqlQuery = f"INSERT INTO business.request " \
                           f"(RequestDate, RequestStatus,  CustomerID, ItemID) " \
                           f"VALUES (DATE('{timing}'), '{requestStatus}', '{username}', {itemInput})"

                mycursor.execute(sqlQuery)
                mysqldb.commit()

                if requestStatus == "Submitted and Waiting for payment":
                    deadline = getDueDate(timing)
                    servicefee = getServiceFeeAmount(itemInput)
                    print(deadline)
                    print(servicefee)
                    nextQuery = f"INSERT INTO business.servicefee " \
                                f"(PaymentCreationDate, DueDate, ServiceFeeAmount, CustomerID, ItemID)" \
                                f"VALUES (DATE('{timing}'), DATE('{deadline}'), {servicefee}, '{username}', {itemInput})"
                    mycursor.execute(nextQuery)
                    print("Created service fee table")
                    mysqldb.commit()

                else:
                    sqlQuery = f"INSERT INTO business.service (ServiceStatus, CustomerID, ItemID) " \
                               f"VALUES ('Waiting for approval', '{username}', {itemInput})"
                    mycursor.execute(sqlQuery)
                    print("Successfully inserted in to Service Table")
                    mysqldb.commit()
                print(successRequestItem)
            else:
                print("Item is already requested for service!")
    except:
        mysqldb.rollback()

    mysqldb.close()


# requestForService('test1')

# This function cancels the customer's request for servicing of their products
def cancelRequest(username):
    noRequestForServicing = "You have not request any item for servicing yet"
    successCancelRequest = "You have successfully cancelled your request"
    try:
        mycursor.execute(
            f"SELECT * FROM business.request WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:
            print(noRequestForServicing)
        else:
            requestId = input(
                "Enter the Request ID that you wish to cancel your request: ")
            mycursor.execute(f"SELECT * FROM business.request WHERE RequestID = {requestId} "
                             f"AND (RequestStatus NOT LIKE 'Approved' AND RequestStatus NOT LIKE 'Cancelled' "
                             f"AND RequestStatus NOT LIKE 'Completed')")
            if len(mycursor.fetchall()) == 0:
                print("Invalid RequestID entered")
            else:
                sqlQuery = f"UPDATE business.request SET RequestStatus = 'Cancelled' WHERE RequestID = {requestId}"
                mycursor.execute(sqlQuery)
                itemIDDelete = getItemIDFromServiceRequest(requestId)
                mycursor.execute(
                    f"DELETE FROM business.service WHERE CustomerID = '{username}' AND ItemID = {itemIDDelete}")
                mysqldb.commit()
                mycursor.execute(
                    f"DELETE FROM business.servicefee WHERE CustomerID = '{username}' AND ItemID = {itemIDDelete}")
                mysqldb.commit()
                print(successCancelRequest)
    except:
        mysqldb.rollback()
    mysqldb.close()


# This function enables the customer to pay for their service fee should they incurred
def payingServicePayment(username):
    noNeedToPay = "There is no Service Payment Required"
    successPaid = "Successfully paid the Service payment"
    dateOfPayment = datetime.datetime.now()
    try:
        mycursor.execute(
            f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:  # Check whether the customer have any service payment to pay
            print(noNeedToPay)
        else:
            requestId = input(
                "Enter the Request ID that you wish to pay your service fee: ")
            mycursor.execute(f"SELECT * FROM business.request WHERE RequestID = {requestId} "
                             f"AND RequestStatus = 'Submitted and Waiting for payment' AND CustomerID = '{username}'")

            if len(mycursor.fetchall()) == 0:
                print("Invalid RequestID entered")
            else:

                itemID = getItemIDFromServiceRequest(requestId)

                mycursor.execute(f"SELECT DueDate FROM business.servicefee WHERE ItemID = {itemID} "
                                 f"AND CustomerID = '{username}'")
                result = list(mycursor.fetchone())

                if dateOfPayment > result[0]:
                    print(
                        "Service is cancelled as the payment date is beyond the due date")
                    sqlQuery = f"UPDATE business.request SET RequestStatus = 'Canceled' " \
                               f"WHERE RequestID = {requestId}"
                    mycursor.execute(sqlQuery)

                    mycursor.execute(
                        f"DELETE FROM business.servicefee WHERE CustomerID = '{username}' AND ItemID = {itemID}")
                    mysqldb.commit()

                elif dateOfPayment <= result[0]:
                    sqlQuery = f"UPDATE business.request SET RequestStatus = 'In Progress' " \
                               f"WHERE RequestID = {requestId}"
                    mycursor.execute(sqlQuery)
                    sqlQuery = f"INSERT INTO business.service (ServiceStatus, CustomerID, ItemID) " \
                               f"VALUES ('Waiting for approval', '{username}', {itemID})"
                    mycursor.execute(sqlQuery)

                    mycursor.execute(
                        f"UPDATE business.servicefee SET PaymentSettlementDate = DATE('{dateOfPayment}')"
                        f"WHERE ItemID = {itemID} "
                        f"AND CustomerID = '{username}'")
                    mysqldb.commit()

                    print("Service fee is paid")

    except:
        mysqldb.rollback()
    mysqldb.close()


##############################    Administrator Function  ##############################################################################

def printProductInventory():
    try:
        query = f"SELECT ProductID, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
                f"s.ProductID = p.ProductID AND s.PurchaseStatus = 'Sold' " \
                f"), (SELECT COUNT(s.ItemID) FROM business.items s WHERE s.ProductID = p.ProductID " \
                f" AND s.PurchaseStatus = 'Unsold') FROM business.products p"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "IID", "Number of 'SOLD' items", "Number of 'UNSOLD' items"]))
        print("\n")
    except:
        mysqldb.rollback()
    mysqldb.close()


def printItemsUnderService():
    try:
        query = f"SELECT ItemID, CustomerID, ServiceStatus FROM business.request WHERE ServiceStatus != 'Completed'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Item ID", "Customer ID", "Service Status"]))
        print("\n")
    except:
        mysqldb.rollback()

    mysqldb.close()


def printCustomerUnpaidServiceFee():
    try:
        query = f"SELECT CustomerID FROM business.servicefee WHERE PaymentSettlementDate IS NULL "
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=["Customer with unpaid service fee"]))
        print("\n")
    except:
        mysqldb.rollback()

    mysqldb.close()


def approveRequest():
    try:
        query = f"SELECT ItemID FROM business.service WHERE ServiceStatus = 'Waiting for approval'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=["ItemID awaiting for approval"]))
        print("\n")

        itemid = input("Input the ItemID to perform servicing: ")
        mycursor.execute(
            f"SELECT * FROM business.service WHERE ItemID = {itemid} AND ServiceStatus = 'Waiting for approval'")
        if emptyCursor(mycursor):
            print("invalid Item ID!")
        else:
            sqlQuery = f"UPDATE business.request SET RequestStatus = 'Completed' " \
                       f"WHERE ItemID = {itemid}"
            mycursor.execute(sqlQuery)
            sqlQuery = f"UPDATE business.service SET ServiceStatus = 'Completed' " \
                       f"WHERE ItemID = {itemid}"
            mycursor.execute(sqlQuery)
            print("Item has completed servicing!")
            mysqldb.commit()
    except:
        mysqldb.rollback()

    mysqldb.close()

# Search Function

# 1 Filter
# simpleSearchModel('Light2', 'admin1')
# simpleSearchProductCategory('Lights', 'test1')
# simpleSearchPrice(200, 'test1')
# simpleSearchColor('Yellow', 'test1')
# simpleSearchFactory('Malaysia', 'admin1')
# simpleSearchProdYear(2016, 'admin1')

# 2 Filters
# simpleSearchProdYearColor(2016, 'Blue', 'admin1')
# simpleSearchProdYearFactory(2016, 'Malaysia', 'admin1')
# simpleSearchProdYearPrice(2016, 150, 'test1')
# simpleSearchColorPrice('Blue', 200, 'admin1')
# simpleSearchFactoryColor('China', 'Blue', 'admin1')
# simpleSearchFactoryPrice('China', 150, 'admin1')

# 3 Filters
# simpleSearchColorProductionYearPrice('Blue', 2016, 200, 'admin1')
# simpleSearchFactoryProductionYearPrice('Malaysia', 2016, 200, 'admin1')
# simpleSearchColorProductionYearFactory('Blue', 2016, 'Malaysia', 'admin1')
# simpleSearchFactoryColorPrice('Malaysia', 'Blue', 200, 'test1')

# 4 Filters
# simpleSearchAllFilter('Blue', 2016, 'Malaysia', 200, 'admin1')

############ Advanced Search Yeshhhhhhhhhhhhhhhhhhhhh ##################################


def inventoryStocksSearch(category, model, color, powersupply, factory, productionYear):
    myquery = {"Category": category,
               "Model": model, "PurchaseStatus": "Unsold"}
    if color != "":
        myquery["Color"] = color
    if powersupply != "":
        myquery["PowerSupply"] = powersupply
    if factory != "":
        myquery["Factory"] = factory
    if productionYear != "":
        myquery["ProductionYear"] = str(productionYear)
    return myItems_col.count_documents(myquery)


def noOfItemSold(category, model, color, powersupply, factory, productionYear):
    myquery = {"Category": category, "Model": model, "PurchaseStatus": "Sold"}
    if color != "":
        myquery["Color"] = color
    if powersupply != "":
        myquery["PowerSupply"] = powersupply
    if factory != "":
        myquery["Factory"] = factory
    if productionYear != "":
        myquery["ProductionYear"] = str(productionYear)
    return myItems_col.count_documents(myquery)


def advancedSearch(username, category, model, price, warranty, color, powersupply, factory, productionYear):
    try:
        myquery = {}
        if category != "":
            myquery["Category"] = category
        if model != "":
            myquery["Model"] = model
        if price != "":
            myquery["Price ($)"] = {'$lte': price}
        if warranty != "":
            myquery["Warranty (months)"] = warranty

        if(isAdministrator(username)):
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            soldProduct = []
            for x in result:
                listInventory.append(inventoryStocksSearch(
                    x["Category"], x["Model"], color, powersupply, factory, productionYear))
                soldProduct.append(noOfItemSold(
                    x["Category"], x["Model"], color, powersupply, factory, productionYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            dataFrame.insert(5, "Number of items Sold", soldProduct, True)
            print(dataFrame)
        else:
            result = list(myProducts_col.find(
                myquery, {"_id": 0, "Cost ($)": 0, "ProductID": 0}))
            dataFrame = pd.DataFrame(result)

            listInventory = []
            for x in result:
                listInventory.append(inventoryStocksSearch(
                    x["Category"], x["Model"], color, powersupply, factory, productionYear))

            dataFrame.insert(4, "Inventory", listInventory, True)
            print(dataFrame)

        option = input("Do you want to search the individual items (Y/N) ? ")
        if option == 'Y':
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            selection = int(input("Select your option: "))
            print("Searching for products...\n")
            searchItem(result, selection, color,
                       powersupply, factory, productionYear)
    except:
        print("Error in search")


def searchItem(stuff, selection, color, powersupply, factory, productionYear):
    try:
        category = stuff[selection]["Category"]
        model = stuff[selection]["Model"]
        myquery = {"Category": category,
                   "Model": model, "PurchaseStatus": "Unsold"}

        if color != "":
            myquery["Color"] = color
        if powersupply != "":
            myquery["PowerSupply"] = powersupply
        if factory != "":
            myquery["Factory"] = factory
        if productionYear != "":
            myquery["ProductionYear"] = str(productionYear)

        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame)
    except:
        print("Invalid option selected")
