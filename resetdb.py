import mysql.connector
import datetime
import sys
import re
import collections
import pymongo
import pprint
import datetime
import time
# from mysqlx.protobuf.mysqlx_resultset_pb2 import DATE
from pymongo import MongoClient
from tabulate import tabulate
from dateutil.relativedelta import relativedelta

class connection:

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

class clearmysqldb:

    def __init__(self):
        pass

    def exec_sql_file(cursor, sql_file):
        print
        "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
        statement = ""

        for line in open(sql_file):
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r';$', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                try:
                    cursor.execute(statement)
                except (OperationalError, ProgrammingError) as e:
                    print
                    "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

                statement = ""

    mysqldb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password')

    mycursor = mysqldb.cursor()

    mysqldelete = "DROP DATABASE IF EXISTS business"
    mycursor.execute(mysqldelete)
    print('Successfully dropped db!')

    filename = 'MySQL Script.sql'
    exec_sql_file(mycursor, filename)
    print('Successfully recreated db!')



class insertmysqldata:

    Customer1 = ('rilwan99', 'Rilwan Tan', '12345678', 'M', 'rilwan@gmail.com', 'Pulau Tekong Camp', '81234567')
    Customer2 = ('jess99', 'Jess Lee', '', 'M', 'jess@gmail.com', 'Sungei Gudong Camp', '82134567')
    Customer3 = ('deshun99', 'Wong De Shun', '12345678', 'M', 'deshun@gmail.com', 'Changi Prison', '91234567')
    Customer4 = ('junding98', 'Lim Jun Ding', '12345678', 'M', 'junding@gmail.com', 'Maju Camp', '92345678')
    Customer5 = ('david98', 'David Liew', '12345678', 'M', 'david@gmail.com', 'Pasir Laba Camp', '93456789')
    Customer6 = ('larvine98', 'Larvine Poh', '12345678', 'M', 'larvine@gmail.com', 'Hendon Camp', '98765432')

    listOfCustomer = [Customer1, Customer2, Customer3, Customer4, Customer5, Customer6]

    # --- Administrator ---
    Admin1 = ('admin1', 'Admin Name1', 'password1', 'M', '92345678')
    Admin2 = ('admin2', 'Admin Name2', 'password2', 'M', '98762345')
    Admin3 = ('admin3', 'Admin Name3', 'password3', 'M', '87650987')
    Admin4 = ('admin4', 'Admin Name4', 'password4', 'M', '98675432')
    Admin5 = ('admin5', 'Admin Name5', 'password5', 'M', '98654337')

    listOfAdmin = [Admin1, Admin2, Admin3, Admin4, Admin5]

    def __init__(self):
        pass

    def addCustomer(listOfTuples):
        strg = ""
        count = 0
        for tup in listOfTuples:
            id, name, password, gender, email, address, phoneNumber = tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]
            newTup = (id,) + (name,) + (password,) + (gender,) + (email,) + (address,) + (phoneNumber,)

            if count == len(listOfTuples) - 1:
                strg += str(newTup)
            else:
                strg += str(newTup) + ", "
            count += 1
        return strg

    def creatingCustomer(listOfTuples):

        mysqldb, mycursor = connection.connectDB()

        try:
            mycursor.execute(
                "INSERT into business.customer (CustomerID, CustomerName, CustomerPassword, Gender, EmailAddress, Address, PhoneNumber)"
                " VALUES " + insertmysqldata.addCustomer(listOfTuples)
            )
            mysqldb.commit()
            print('Customer Records inserted successfully!')
        except:
            print('Failed to insert Customer records!')
            mysqldb.rollback()

    def addAdmin(listOfTuples):
        strg = ""
        count = 0
        for tup in listOfTuples:
            id, name, gender, phoneNumber, password = tup[0], tup[1], tup[2], tup[3], tup[4]
            newTup = (id,) + (name,) + (gender,) + (phoneNumber,) + (password,)
            if count == len(listOfTuples) - 1:
                strg += str(newTup)
            else:
                strg += str(newTup) + ", "
            count += 1
        return strg

    def creatingAdmin(listOfTuples):

        mysqldb, mycursor = connection.connectDB()

        try:
            mycursor.execute(
                "INSERT into business.administrator (AdministratorID, AdministratorName, AdministratorPassword, Gender, PhoneNumber)"
                " VALUES " + insertmysqldata.addAdmin(listOfTuples)
            )
            mysqldb.commit()
            print('Admin Records inserted successfully!')
        except:
            print('Failed to insert Admin records!')
            mysqldb.rollback()


class ImportProductsItems:

    # Import the item dataset from MongoDB to MySQL
    def ItemImports():

        myItems_col, myProducts_col = connection.connectMongo()
        mysqldb, mycursor = connection.connectDB()

        def getProductID(model, category):

            result = myProducts_col.find({"Model": model, "Category": category})
            listofstuff = list(result)
            return listofstuff[0]['ProductID']

        lst_importable = []
        cursor = myItems_col.find({}, {"ItemID": 1, "Category": 1, "Color": 1, "Factory": 1, "PowerSupply": 1,
                                       "PurchaseStatus": 1, "ProductionYear": 1, "Model": 1, "ServiceStatus": 1})
        for cur in cursor:
            try:
                data = (cur['ItemID'], cur['PurchaseStatus'], str(getProductID(cur['Model'], cur['Category'])))
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

        myItems_col, myProducts_col = connection.connectMongo()
        mysqldb, mycursor = connection.connectDB()

        # Calculating the inventory Stocks
        def inventoryStocks(category, model):
            return myItems_col.count_documents({"Category": category, "Model": model, "PurchaseStatus": "Unsold"})

        lst_importable = []
        cursor = myProducts_col.find({}, {"Category": 1, "Cost ($)": 1, "Model": 1, "Price ($)": 1, "ProductID": 1,
                                          "Warranty (months)": 1})
        for cur in cursor:
            try:
                data = (str(cur['ProductID']), cur['Category'], cur['Model'], str(cur['Price ($)']), str(cur['Cost ($)']),
                        str(cur['Warranty (months)']),
                        str(inventoryStocks(cur["Category"], cur["Model"])))
                lst_importable.append(data)
            except:
                continue
        query = '''INSERT INTO business.products(ProductID, Category, Model, Price, Cost, Warranty, Inventory) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        mycursor.executemany(query, lst_importable)
        mysqldb.commit()
        print("Successfully imported " + str(len(lst_importable)) + " products!")
        mysqldb.close()

def resetdb():
    clearmysqldb()
    insertmysqldata.creatingCustomer(insertmysqldata.listOfCustomer)
    insertmysqldata.creatingAdmin(insertmysqldata.listOfAdmin)
    ImportProductsItems.ProductImports()
    ImportProductsItems.ItemImports()


if __name__ == "__main__":
    resetdb()
