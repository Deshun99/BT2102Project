from utilities import *
from customer import *
from administrator import *
import mysql.connector
import sys
import re
import collections
import pymongo
import pprint
from pymongo import MongoClient
import datetime
import time
from tabulate import tabulate
from dateutil.relativedelta import relativedelta
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)
myItems_col, myProducts_col = connectMongo()

#registerAdministrator("jess99", "Daud Ali Aser", "12345678", "M", "81234567")
#if (loginAdministrator('jess99','12345678')):
   # print("yes")
#
#  if (loginCustomer("jess99", "12345678")):
#    print("yes customer")

# requestForService(1)
# payingServicePayment(1)
# cancelRequest(1)
# if checkoutItem("jess99", 1101):
#     print('yes')
# else: 
#     print('no')

# print(simple_search_id('1001'))
# basicProductSearchByCategory('Lights')
# basicProductFilterByFactory('Malaysia')
# basicProductFilterByProductionYear('2019')
# loginCustomer("david98", "12345678")
# displayAdminRecords()
# displayProduct()
# print(searchByCategory("Light1"))
# print(simpleSearchId("1001"))

## Search Function






advancedSearch("jess99", "", "","", "", "", "", "", "")