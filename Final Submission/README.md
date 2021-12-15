# Online Smart Home Ecommerce System (OSHES)
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img alt="MySQL" src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white"/> ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![Tkinter](https://img.shields.io/badge/Tkinter-%234ea94b.svg?style=for-the-badge&logo=tkinter&logoColor=orange)
## About

With the advent and popularity of ecommerce, more and more consumers are purchasing smart-home equipment online. A company that focuses its business on smart home equipment has decided to incorporate a new Online Smart Home Ecommerce System. The company’s in-house IT team is expected to deliver a database software application (named “OSHES”) to manage product sales, administration, and maintenance.

## Details
_This project is part of the module BT2102: Data Management and Visualisation assignment 1, where students are tasked to create an OSHES (Online Smart Home Ecommerce System) using only python, MySQL and MongoDB_

Lights and Locks sells state of the art Lights and Locks. Customers can search for products based on product category and model and specify product and item attributes when searching before purchasing a Light or a Lock. Customers can also send their purchased items for servicing, but will have to pay a service fee IF they request to service an item that is out of warranty. As an added feature, customers can request to service the item more than one time. Customers can also cancel their requests, but not when the item is already undergoing servicing by the Admin.

Meanwhile, Admins can also search for products like customers but will get to see more information on the items like how much it cost to produce the item. Admins can also approve of requests and can choose to service those approved requests.

# Setup 
to install dependencies


```pip install -r requirements.txt```

Ensure that MySQL is set up locally with the following credentials:
```
user: 'root'
password: 'password'
port: 3306
mysql_db: 'business'
host: '127.0.0.1'
```

Ensure that MongoDB is set up locally with the following credentials:
```
mongo_uri: 'mongodb://127.0.0.1:27017/'
cluster_name: 'admin'
```

# Usage
Make sure you have python version 3.7.5 and above

**Make sure your console starts off from this before performing the commands below**
```
.../GRP-05-AS1/
```

1) open the file 'oshes.py'
2) open a seperate terminal and perform the following command to reset the database
```
resetdb.py 
```
3) run the OSHES system with the following command
```
oshes.py
```

# Tech Stack
| Libraries and Frameworks Used| Backend/Frontend     |
| ----------- | ---------- |
| Tkinter     | Frontend GUI |
| MySQL   | Database |
| MongoDB | Database |
