from utilities import *
from customer import *
from administrator import *
from pymongo import MongoClient
#from tabulate import tabulate
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

########################################################### Login & Registration Function ###########################################################


def loginAdministrator(adminID, password):

    mysqldb, mycursor = connectDB()

    try:
        mycursor.execute(
            f"SELECT * FROM business.administrator WHERE AdministratorID = '{adminID}' AND AdministratorPassword = '{password}'")
        if emptyCursor(mycursor):
            return False
        else:
            return True
    except:
        mysqldb.rollback()
    mysqldb.close()


def registerAdministrator(adminID, name, password, gender, phoneNumber):

    mysqldb, mycursor = connectDB()
    userIDisUsed = "AdminID is already taken please select a different AdminID"
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


############################################### Administrator Functions ###############################################

def printProductInventory():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT ProductID, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
                f"s.ProductID = p.ProductID AND s.PurchaseStatus = 'Sold' " \
                f"), (SELECT COUNT(s.ItemID) FROM business.items s WHERE s.ProductID = p.ProductID " \
                f"AND s.PurchaseStatus = 'Unsold') FROM business.products p"
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(type(result))

        print(tabulate(result, headers=[
              "IID", "Number of 'SOLD' items", "Number of 'UNSOLD' items"]))
        print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def printSoldProduct():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT ProductID, Category, Model, (SELECT COUNT(s.ItemID) FROM business.items s WHERE " \
                f"s.ProductID = p.ProductID AND s.PurchaseStatus = 'Sold' " \
                f") FROM business.products p"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "ProductID", "Category", "Model", "Number of 'SOLD' items"]))
        print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def printServicedItem(adminID):

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT RequestID, ItemID FROM business.service WHERE AdministratorID = '{adminID}'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        # print(tabulate(result, headers=[
        #       "ServiceID", "CustomerID", "ItemID", "RequestID"]))
        # print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def printPendingRequest():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:

        query = f"SELECT RequestID, RequestStatus, ItemID, CustomerID FROM business.request WHERE (RequestStatus LIKE 'Submitted' OR RequestStatus LIKE 'In Progress')"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Request ID", "RequestStatus", "ItemID", "CustomerID"]))
        print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def printItemsUnderService():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:

        query = f"SELECT ItemID, ServiceStatus FROM business.items WHERE ServiceStatus != ''"
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=["Item ID", "Service Status"]))
        print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def printCustomerUnpaidServiceFee():

    from tabulate import tabulate
    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT CustomerID , RequestID FROM business.servicefee WHERE PaymentSettlementDate IS NULL "
        mycursor.execute(query)
        result = mycursor.fetchall()

        print(tabulate(result, headers=[
              "Customer ID", "RequestID"]))
        print("\n")
        return list(result)
    except:
        mysqldb.rollback()
    mysqldb.close()


def approveRequest(adminID, requestID):

    mysqldb, mycursor = connectDB()

    try:
        # query = f"SELECT ItemID FROM business.items WHERE ServiceStatus = 'Waiting for approval'"
        # mycursor.execute(query)
        # result = mycursor.fetchall()

        from utilities import getItemIDFromServiceRequest

        itemid = getItemIDFromServiceRequest(requestID)

        mycursor.execute(
            f"SELECT * FROM business.items WHERE ItemID = {itemid} AND ServiceStatus = 'Waiting for approval'")
        if emptyCursor(mycursor):
            print("invalid Item ID!")
            return False
        else:
            sqlQuery = f"UPDATE business.request SET RequestStatus = 'In Progress' " \
                       f"WHERE RequestID = {requestID}"
            mycursor.execute(sqlQuery)
            sqlQuery = f"UPDATE business.service SET AdministratorID = '{adminID}'" \
                       f"WHERE RequestID = {requestID}"
            mycursor.execute(sqlQuery)
            sqlQuery = f"UPDATE business.items SET ServiceStatus = 'In Progress' " \
                       f"WHERE ItemID = {itemid}"
            mycursor.execute(sqlQuery)
            print("Request for the item is approved")
            mysqldb.commit()

            return serviceItem(requestID)
    except:
        mysqldb.rollback()
        print("failed to approve request")

    mysqldb.close()


def serviceItem(requestID):

    mysqldb, mycursor = connectDB()

    try:
        query = f"SELECT ItemID FROM business.items WHERE ServiceStatus = 'In Progress'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        # print(tabulate(result, headers=["ItemID awaiting for service"]))
        # print("\n")

        from utilities import getItemIDFromServiceRequest

        itemid = getItemIDFromServiceRequest(requestID)

        mycursor.execute(
            f"SELECT * FROM business.items WHERE ItemID = {itemid} AND ServiceStatus = 'In Progress'")
        if emptyCursor(mycursor):
            print("invalid Item ID!")
            return False
        else:
            sqlQuery = f"UPDATE business.request SET RequestStatus = 'Completed' " \
                       f"WHERE RequestID = {requestID}"
            mycursor.execute(sqlQuery)
            sqlQuery = f"UPDATE business.items SET ServiceStatus = 'Completed' " \
                       f"WHERE ItemID = {itemid}"
            mycursor.execute(sqlQuery)
            print("Item has completed servicing!")
            mysqldb.commit()
            return True
    except:
        mysqldb.rollback()

    mysqldb.close()
