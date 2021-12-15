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

from tkinter.constants import FALSE, TRUE
from tkinter import *


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

################################## MISC Function ###########################################################

def retrieveCustomerID(username) :

    mysqldb, mycursor = connectDB()

    mycursor.execute(
        f"SELECT * FROM customer WHERE CustomerID = '{username}'")
    cursor = mycursor.fetchall()
    return cursor[0][0]

################################## Login & Registration Function ###########################################################

def loginCustomer(userID, password) :

    mysqldb, mycursor = connectDB()

    try:

        mycursor.execute(f"SELECT * FROM business.customer WHERE CustomerID = '{userID}' AND CustomerPassword = '{password}'")
        if emptyCursor(mycursor):
            print("its false")
            return False
        else:
            print("its true")
            return True
    except:
        mysqldb.rollback()
        print("did not work")
    mysqldb.close()


def registerCustomer(userID, name, password, gender, emailAddress, address, phoneNumber):

    mysqldb, mycursor = connectDB()
    userIDisUsed = "UserID is already taken please select a different UserID"
    successRegistered = "Successfully registered as a customer"

    try:
        mycursor.execute(f"SELECT * FROM business.customer WHERE CustomerID = '{userID}'")
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