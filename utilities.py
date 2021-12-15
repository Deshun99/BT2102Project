from utilities import *
from customer import *
from administrator import *
from pymongo import MongoClient
from tabulate import tabulate
from dateutil.relativedelta import relativedelta
import mysql.connector
import sys
import re
import collections
import pymongo
import pprint
import datetime
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
# from dns.tsig import sign


###################################### CONNECT TO DB FUNCTIONS ######################################################

def connectDB():
    import mysql.connector

    mysqldb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password',
        db='business')

    mycursor = mysqldb.cursor()

    return mysqldb, mycursor


def connectMongo():
    from pymongo import MongoClient

    myclient = MongoClient("mongodb://127.0.0.1:27017/")
    mydb_Business = myclient["Business"]
    myItems_col = mydb_Business["items"]
    myProducts_col = mydb_Business["products"]

    return myItems_col, myProducts_col


###################################### COMMON FUNCTIONS ######################################################

def emptyCursor(mycursor):

    return len(mycursor.fetchall()) == 0

# Prints out the list of items purchased by the customer


def printPurchasedList(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

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

###################################### DISPLAY RECORDS ###########################################################


def displayCustomerRecords():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        mycursor.execute("SELECT * from customer")
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Customer ID", "name", "gender", "email address", "phone number", "address", "password"]))
    except:
        print('Error: Unable to fetch data.')
        mysqldb.close()


def displayAdminRecords():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        mycursor.execute("SELECT * from administrator")
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Administrator ID", "name", "gender", "phone number", "password"]))
    except:
        print('Error: Unable to fetch data.')
        mysqldb.close()


def displayProduct():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT Category, Model, Price, Warranty, Inventory FROM business.products"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(tabulate(result, headers=[
              "Category", "Model", "Price ($)", "Warranty (months)", "Inventory"]))
    except:
        mysqldb.rollback()
        mysqldb.close()


###################################### MONGOL DB SEARCH FUNCTION ######################################################

def isAdministrator(username):

    mysqldb, mycursor = connectDB()

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


def inventoryStocksSearch(category, model, color, powersupply, factory, productionYear):

    myItems_col, myProducts_col = connectMongo()

    myquery = {"Category": category,
               "Model": model, "PurchaseStatus": "Unsold"}
    if color != "-":
        myquery["Color"] = color
    if powersupply != "-":
        myquery["PowerSupply"] = powersupply
    if factory != "-":
        myquery["Factory"] = factory
    if productionYear != "-":
        myquery["ProductionYear"] = str(productionYear)

    return myItems_col.count_documents(myquery)


def noOfItemSold(category, model, color, powersupply, factory, productionYear):

    myItems_col, myProducts_col = connectMongo()

    myquery = {"Category": category, "Model": model, "PurchaseStatus": "Sold"}
    if color != "-":
        myquery["Color"] = color
    if powersupply != "-":
        myquery["PowerSupply"] = powersupply
    if factory != "-":
        myquery["Factory"] = factory
    if productionYear != "-":
        myquery["ProductionYear"] = str(productionYear)

    return myItems_col.count_documents(myquery)


def searchItem(category, model, color, warranty, powersupply, factory, productionYear):
    import pandas as pd
    pd.set_option('display.min_rows', 50)
    pd.set_option('display.expand_frame_repr', True)
    myItems_col, myProducts_col = connectMongo()

    try:
        # category = stuff[selection]["Category"]
        # model = stuff[selection]["Model"]
        myquery = {"PurchaseStatus": "Unsold"}

        if category != "-":
            myquery["Category"] = category
        if model != "-":
            myquery["Model"] = model
        if warranty != "-":
            myquery["Warranty (months)"] = int(warranty)
        if color != "-":
            myquery["Color"] = color
        if powersupply != "-":
            myquery["PowerSupply"] = powersupply
        if factory != "-":
            myquery["Factory"] = factory
        if productionYear != "-":
            myquery["ProductionYear"] = str(productionYear)

        result = myItems_col.find(
            myquery, {"_id": 0, "ServiceStatus": 0, "PurchaseStatus": 0})
        dataFrame = pd.DataFrame(result)
        print(dataFrame, "\n")
        return dataFrame
    except:
        print("Invalid option selected, please select valid option", "\n")


def advancedSearch(username, category, model, price, warranty, color, powersupply, factory, productionYear):

    import pandas as pd
    myItems_col, myProducts_col = connectMongo()

    def checksearch():
        option = input("Do you want to search the individual items (Y/N) ?")
        print("")
        if (option == 'Y'):
            print("There are a total of " + str(len(result)) +
                  " products to select your item")
            print("Please choose from option 0 to " +
                  str(len(result) - 1), "\n")
            selection = int(input("Select your option: "))
            print("")
            print("Searching for products...\n")
            searchItem(result, selection, color, warranty,
                       powersupply, factory, productionYear)

        elif (option == 'N'):
            print("Search cancelled")
            print("Thank you and good bye")

        else:
            print("Invalid input")
            checksearch()

    try:
        myquery = {}
        if category != "-":
            myquery["Category"] = category
        if model != "-":
            myquery["Model"] = model
        if price != "-":
            if price == "Below $100":
                price1 = 0
                price2 = 100
            if price == "$100-$150":
                price1 = 100
                price2 = 150
            elif price == "$150-$200":
                price1 = 150
                price2 = 200
            myquery["Price ($)"] = {'$gte': price1, '$lte': price2}
        if warranty != "-":
            myquery["Warranty (months)"] = int(warranty)

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
            return dataFrame
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
            return dataFrame

    except:
        print("Error in search", "\n")


def itemSearch(username, itemId):

    import pandas as pd
    myItems_col, myProducts_col = connectMongo()

    myquery = {"ItemID": str(itemId)}

    if (isAdministrator(username)):

        try:

            result = list(myItems_col.find(myquery, {"_id": 0}))
            dataFrame = pd.DataFrame(result)
            print(dataFrame)
            return dataFrame

        except:
            print("Error in search", "\n")

    else:
        print("Not Administrator, cancelling item ID search")


#################################### WARRANTY, SERVICE AND PAYMENTS ####################################################

# Prints out the list of items under servicing for customer
def printItemServicingList(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT ItemID, RequestStatus FROM business.request WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Request ID", "Request Date", "Request Status", "Customer ID", "Item ID"]))
        print("\n")
        return list(result)

    except:
        mysqldb.rollback()
    mysqldb.close()


def printItemIDServicingList(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT RequestID, RequestStatus, ItemID FROM business.request WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Request ID", "Request Date", "Request Status", "Service Status", "Customer ID", "Item ID"]))
        print(result)
        return list(result)

    except:
        mysqldb.rollback()
    mysqldb.close()

# Prints out the list of items purchased by a customer


def getPurchasedItems(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT ItemID FROM business.purchased WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=["Item ID"]))
        print("\n")
        return list(result)

    except:
        mysqldb.rollback()
    mysqldb.close()


def getPurchasedItemsFull(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT * FROM business.purchased WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Customer ID", "Item ID", "Purchase Date", "Warranty End Date"]))
        print("\n")
        return list(result)

    except:
        mysqldb.rollback()
    mysqldb.close()


# Prints out the list of items pending for service payment for the customer
def printServicePayment(username):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT RequestID, DueDate, ServiceFeeAmount FROM business.servicefee WHERE CustomerID = '{username}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Request ID", "Due Date", "Service Fee Amount"]))
        print("\n")
        return list(result)

    except:
        mysqldb.rollback()
    mysqldb.close()

# Obtain the warranty end date when customer purchase the item


def getWarrantyEndDate(date, item):

    from dateutil.relativedelta import relativedelta
    import datetime

    mysqldb, mycursor = connectDB()

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
    from dateutil.relativedelta import relativedelta
    import datetime

    return date + datetime.timedelta(days=10)

# Obtaining the service fee amount that the customer needs to pay for


def getServiceFeeAmount(item):

    mysqldb, mycursor = connectDB()

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

# This function checks whether the item purchased by customer is still under warranty


def checkWarranty(itemid, time):

    mysqldb, mycursor = connectDB()

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

    mysqldb, mycursor = connectDB()

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

    mysqldb, mycursor = connectDB()

    try:
        myquery = f"SELECT RequestID FROM business.request WHERE ItemID = {itemid} AND CustomerID = '{customer}'"
        mycursor.execute(myquery)
        result = mycursor.fetchall()
        retrieveID = result

        return retrieveID
    except:
        mysqldb.rollback()

    mysqldb.close()

# This method does not work


def creatingServicePayment(username, timing):

    mysqldb, mycursor = connectDB()

    mycursor.execute(f"SELECT (RequestID, ItemID) FROM business.request WHERE CustomerID = '{username}'"
                     f"AND RequestStatus = 'Submitted and Waiting for payment'")
    if not (emptyCursor(mycursor)):
        result = mycursor.fetchall()
        listOfID = list(result)
        print(listOfID)
        for row in listOfID:
            requestid = row[0]
            dueDate = getDueDate(timing)
            serviceFee = getServiceFeeAmount(row[1])

            mycursor.execute(
                f"SELECT * FROM business.servicepayment WHERE RequestID = {requestid}")
            if emptyCursor(mycursor):
                newQuery = f"INSERT INTO business.servicepayment " \
                           f"(PaymentCreationDate, DueDate, ServiceFeeAmount, RequestID, CustomerID) VALUES " \
                           f"(DATE('{timing}'), DATE('{dueDate}'), " \
                           f"{serviceFee}, {requestid}, '{username}')"
                mycursor.execute(newQuery)

                mysqldb.commit()

        print("Successfully inserted into Service Payment Table")

# This function is meant for customers to view their service payment


def viewServicePayment(username):

    mysqldb, mycursor = connectDB()

    noServicePayment = "You do not have any service payment to settle"
    try:
        mycursor.execute(
            f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:
            print(noFineMsg)
        else:
            mycursor.execute(
                f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
            result = mycursor.fetchall()
            print(tabulate(result, headers=[
                  "Payment Creation Date", "Due Date", "Service Fee", "Request ID", "Customer ID"]))
            print("\n")
    except:
        mysqldb.rollback()
    mysqldb.close()


def getItemIDFromServiceRequest(request):

    mysqldb, mycursor = connectDB()

    try:
        mycursor.execute(
            f"SELECT ItemID FROM business.request WHERE RequestID = {request}")
        result = list(mycursor.fetchone())
        return result[0]
    except:
        mysqldb.rollback()

    mysqldb.close()


def getRequestIDFromServiceRequest(itemID):
    mysqldb, mycursor = connectDB()

    try:
        mycursor.execute(
            f"SELECT RequestID FROM business.request WHERE ItemID = {itemID} AND (RequestStatus LIKE 'Submitted' OR RequestStatus LIKE 'Submitted and Waiting for payment')")
        result = list(mycursor.fetchone())
        return result[0]
    except:
        mysqldb.rollback()

    mysqldb.close()

# This function facilitates the customer's request for servicing of their products


def requestForService(username, itemID):

    mysqldb, mycursor = connectDB()

    successRequestItem = "You have successfully requested for servicing"
    timing = datetime.datetime.now()

    try:
        itemInput = itemID

        mycursor.execute(
            f"SELECT * FROM business.purchased WHERE ItemID = {itemInput}")
        if emptyCursor(mycursor):
            errorMsg = "Invalid ItemID input"
            print(errorMsg)
            return False
        else:
            mycursor.execute(f"SELECT * FROM business.request "
                             f"WHERE ItemID = {itemInput} AND (RequestStatus LIKE 'Approved' OR RequestStatus LIKE 'Submitted' OR RequestStatus LIKE 'Submitted and Waiting for payment' OR RequestStatus LIKE 'In Progress')")
            if emptyCursor(mycursor):

                requestStatus = checkWarranty(itemInput, timing)
                # serviceStatus = checkServiceStatus(itemInput, timing)

                sqlQuery = f"INSERT INTO business.request " \
                           f"(RequestDate, RequestStatus, CustomerID, ItemID) " \
                           f"VALUES (DATE('{timing}'), '{requestStatus}', '{username}', {itemInput})"

                mycursor.execute(sqlQuery)
                mysqldb.commit()

                requestID = getRequestIDFromServiceRequest(itemInput)

                print(requestID)

                if requestStatus == "Submitted and Waiting for payment":
                    deadline = getDueDate(timing)
                    servicefee = getServiceFeeAmount(itemInput)
                    print(deadline)
                    print(servicefee)
                    nextQuery = f"INSERT INTO business.servicefee " \
                                f"(PaymentCreationDate, DueDate, ServiceFeeAmount, CustomerID, RequestID)" \
                                f"VALUES (DATE('{timing}'), DATE('{deadline}'), {servicefee}, '{username}', {requestID})"
                    mycursor.execute(nextQuery)
                    print(
                        "Your Warranty has expired please pay your servicefee within the deadline")
                    mysqldb.commit()

                else:
                    sqlQuery = f"INSERT INTO business.service (ItemID, RequestID) " \
                               f"VALUES ({itemInput}, {requestID})"
                    mycursor.execute(sqlQuery)

                    sqlQuery = f"UPDATE business.items SET ServiceStatus = 'Waiting for approval' WHERE ItemID = {itemInput}"
                    mycursor.execute(sqlQuery)
                    print("Successfully inserted in to Service Table")
                    mysqldb.commit()

                print(successRequestItem)
                return True
            else:
                notice = "Request has already been submitted for the item!"
                print(notice)
                return False
    except:
        mysqldb.rollback()
    mysqldb.close()


# This function cancels the customer's request for servicing of their products
def cancelRequest(username, requestID):

    mysqldb, mycursor = connectDB()

    noRequestForServicing = "You have not request any item for servicing yet"
    successCancelRequest = "You have successfully cancelled your request"
    try:
        mycursor.execute(
            f"SELECT * FROM business.request WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:
            print(noRequestForServicing)
            return False
        else:
            # mycursor.execute(f"SELECT * FROM business.request WHERE RequestID = {requestId} "

            # requestId = input(
            #     "Enter the Request ID that you wish to cancel your request: ")
            mycursor.execute(f"SELECT * FROM business.request WHERE RequestID = {requestID} "
                             f"AND (RequestStatus NOT LIKE 'Approved' AND RequestStatus NOT LIKE 'Cancelled' "
                             f"AND RequestStatus NOT LIKE 'Completed')")
            if len(mycursor.fetchall()) == 0:
                invalidID = "Invalid ItemID entered"
                print(invalidID)
                return False
            else:
                sqlQuery = f"UPDATE business.request SET RequestStatus = 'Cancelled' WHERE RequestID = {requestID}"
                mycursor.execute(sqlQuery)
                itemIDDelete = getItemIDFromServiceRequest(requestID)
                mycursor.execute(
                    f"DELETE FROM business.service WHERE RequestID = {requestID}")
                mysqldb.commit()
                mycursor.execute(
                    f"DELETE FROM business.servicefee WHERE CustomerID = '{username}' AND RequestID = {requestID}")
                mysqldb.commit()
                sqlQuery = f"UPDATE business.items SET ServiceStatus = '' WHERE ItemID = {itemIDDelete}"
                mycursor.execute(sqlQuery)
                print(successCancelRequest)
                return True
    except:
        mysqldb.rollback()
    mysqldb.close()


# This function enables the customer to pay for their service fee should they incurred // Change to accept Request ID
def payingServicePayment(username, requestId):

    mysqldb, mycursor = connectDB()

    noNeedToPay = "There is no Service Payment Required"
    successPaid = "Successfully paid the Service payment"
    dateOfPayment = datetime.datetime.now()
    try:
        mycursor.execute(
            f"SELECT * FROM business.servicefee WHERE CustomerID = '{username}'")
        if len(mycursor.fetchall()) == 0:  # Check whether the customer have any service payment to pay
            print(noNeedToPay)
            return False
        else:
            mycursor.execute(f"SELECT * FROM business.request WHERE RequestID = {requestId} "
                             f"AND RequestStatus = 'Submitted and Waiting for payment' AND CustomerID = '{username}'")

            if len(mycursor.fetchall()) == 0:
                print("Invalid RequestID entered")
                return False
            else:

                itemId = getItemIDFromServiceRequest(requestId)

                mycursor.execute(f"SELECT DueDate FROM business.servicefee WHERE RequestID = {requestId} "
                                 f"AND CustomerID = '{username}'")
                result = list(mycursor.fetchone())

                if dateOfPayment > result[0]:
                    print(
                        "Service is cancelled as the payment date is beyond the due date")
                    sqlQuery = f"UPDATE business.request SET RequestStatus = 'Cancelled' " \
                               f"WHERE RequestID = {requestId}"
                    mycursor.execute(sqlQuery)

                    mycursor.execute(
                        f"DELETE FROM business.servicefee WHERE CustomerID = '{username}' AND RequestID = {requestId}")
                    mysqldb.commit()

                elif dateOfPayment <= result[0]:
                    sqlQuery = f"UPDATE business.request SET RequestStatus = 'In Progress' " \
                               f"WHERE RequestID = {requestId}"
                    mycursor.execute(sqlQuery)
                    sqlQuery = f"INSERT INTO business.service (ItemID, RequestID) " \
                               f"VALUES ({itemId}, {requestId})"
                    mycursor.execute(sqlQuery)

                    sqlQuery = f"UPDATE business.items SET ServiceStatus = 'Waiting for approval' WHERE ItemID = {itemId}"
                    mycursor.execute(sqlQuery)

                    mycursor.execute(
                        f"UPDATE business.servicefee SET PaymentSettlementDate = DATE('{dateOfPayment}')"
                        f"WHERE RequestID = {requestId} "
                        f"AND CustomerID = '{username}'")
                    mysqldb.commit()

                    print("Service fee is paid")
                    return True

    except:
        mysqldb.rollback()
    mysqldb.close()

################################################# SEARCH AND CHECKOUT ##################################################

# This function enable customers to checkout their items


def checkoutItem(username, itemID):

    mysqldb, mycursor = connectDB()

    itemNotAvailable = "Item is not available or already sold!"

    timing = datetime.datetime.now()

    successPurchaseItem = "You have successfully purchased the item"

    try:
        mycursor.execute(
            f"SELECT * FROM business.items WHERE ItemID = '{itemID}' AND PurchaseStatus = 'Unsold'")
        if emptyCursor(mycursor):
            return False
        else:
            sqlQuery = f"INSERT INTO business.purchased " \
                       f"VALUES('{username}', {itemID}, DATE('{timing}'), DATE('{getWarrantyEndDate(timing, itemID)}'))"
            mycursor.execute(sqlQuery)

            updateQuery = f"UPDATE items SET PurchaseStatus = 'Sold' WHERE ItemID = '{itemID}'"
            mycursor.execute(updateQuery)

            print("Item table is updated successfully!")
            mysqldb.commit()
            print(successPurchaseItem)
            return True
    except:
        mysqldb.rollback()
    mysqldb.close()


# def basicProductSearchByCategory(category):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM business.products WHERE Category = '{category}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print("\n")
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailable(listOfProd, int(selection) - 1)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def basicProductSearchByModel(model):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM products WHERE Model = '{model}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print("\n")
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailable(listOfProd, int(selection) - 1)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def listOfItemAvailable(keyword, index):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT ItemID, Category, Color, Factory, PowerSupply, Model, ProductionYear " \
#                 f"FROM business.items s WHERE s.Category = '{keyword[index][0]}' AND s.Model = '{keyword[index][1]}' " \
#                 f"AND s.PurchaseStatus = 'Unsold'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         if len(list(result)) > 0:
#             print(tabulate(result, headers=["ItemID", "Category", "Color", "Factory", "PowerSupply",
#                                             "Model", "Production Year"]))
#             print("\n")
#         else:
#             print("There are no items available\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def basicProductFilterByPrice(price):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, Inventory FROM business.products WHERE Price <= {price}"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print('\n')
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailable(listOfProd, int(selection) - 1)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def basicProductFilterByColor(color):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
#                 f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
#                 f"AND s.Color = '{color}') FROM business.products p"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print("\n")
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailableByColor(
#                     listOfProd, int(selection) - 1, color)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def listOfItemAvailableByColor(keyword, index, color):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT ItemID, Category, Color, Factory, PowerSupply, Model, ProductionYear " \
#                 f"FROM items s WHERE s.Category = '{keyword[index][0]}' AND s.Model = '{keyword[index][1]}' " \
#                 f"AND s.PurchaseStatus = 'Unsold' AND s.Color = '{color}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         if len(list(result)) > 0:
#             print(tabulate(result, headers=["ItemID", "Category", "Color", "Factory", "PowerSupply",
#                                             "Model", "Production Year"]))
#             print("\n")
#         else:
#             print("There are no items available\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def basicProductFilterByFactory(factory):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
#                 f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
#                 f"AND s.Factory = '{factory}') FROM business.products p"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print("\n")
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailableByFactory(
#                     listOfProd, int(selection) - 1, factory)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def listOfItemAvailableByFactory(keyword, index, factory):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT ItemID, Category, Color, Factory, PowerSupply, Model, ProductionYear " \
#                 f"FROM business.items s WHERE s.Category = '{keyword[index][0]}' AND s.Model = '{keyword[index][1]}' " \
#                 f"AND s.PurchaseStatus = 'Unsold' AND s.Factory = '{factory}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         if len(list(result)) > 0:
#             print(tabulate(result, headers=["ItemID", "Category", "Color", "Factory", "PowerSupply",
#                                             "Model", "Production Year"]))
#             print("\n")
#         else:
#             print("There are no items available\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def basicProductFilterByProductionYear(productionYear):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT Category, Model, Price, Warranty, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
#                 f"s.Category = p.Category AND s.Model = p.Model AND s.PurchaseStatus = 'Unsold' " \
#                 f"AND s.ProductionYear = '{productionYear}') FROM business.products p"
#         mycursor.execute(query)
#         result = mycursor.fetchall()

#         if len(list(result)) > 0:
#             print(tabulate(result, headers=[
#                   "Product Category", "Model", "Price", "Warranty", "Inventory"]))
#             print("\n")
#             listOfProd = list(result)
#             option = input(
#                 "Do you want to search the individual items (Y/N) ? ")
#             if option == 'Y':
#                 print("There are a total of " + str(len(result)) +
#                       " products to select your item")
#                 selection = input("Select your option: ")
#                 print("Searching for products...\n")
#                 listOfItemAvailableByProductionYear(
#                     listOfProd, int(selection) - 1, productionYear)
#         else:
#             print("Invalid search\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def listOfItemAvailableByProductionYear(keyword, index, productionYear):

#     from tabulate import tabulate
#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT ItemID, Category, Color, Factory, PowerSupply, Model, ProductionYear " \
#                 f"FROM business.items s WHERE s.Category = '{keyword[index][0]}' AND s.Model = '{keyword[index][1]}' " \
#                 f"AND s.PurchaseStatus = 'Unsold' AND s.ProductionYear = '{productionYear}'"
#         mycursor.execute(query)
#         result = mycursor.fetchall()
#         if len(list(result)) > 0:
#             print(tabulate(result, headers=["ItemID", "Category", "Color", "Factory", "PowerSupply",
#                                             "Model", "Production Year"]))
#             print("\n")
#         else:
#             print("There are no items available\n")
#     except:
#         mysqldb.rollback()
#     mysqldb.close()


# def simple_search_id(id):

#     mysqldb, mycursor = connectDB()

#     try:
#         query = f"SELECT * FROM business.items WHERE ItemID = '{id}' AND PurchaseStatus = 'Sold'"
#         mycursor.execute(query)
#         result = mycursor.fetchone()
#         if len(list(result)) > 0:
#             return list(result)[0]
#         else:
#             return 0
#     except:
#         mysqldb.rollback()
#     mysqldb.close()
