#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install mysql-connector-python installs python connector 
import mysql.connector
from mysql.connector import Error


class Database():
    def __init__(self, host="localhost", port="3306", database="banks_portal", user='root', password='root'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )

            if self.connection.is_connected():
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def getAllAccounts(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "select * from accounts"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def getAllTransactions(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "select * from Transactions"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

#     def deposit(self):
#         if self.connection.is_connected():
#             self.cursor = self.connection.cursor()
#             query = "select * from Transactions where transactionType ='deposit'"
#             self.cursor.execute(query)
#             records = self.cursor.fetchall()
#             return records

#     def withdraw(self):
#         if self.connection.is_connected():
#             self.cursor = self.connection.cursor()
#             query = "select * from Transactions where transactionType = 'withdraw' "
#             self.cursor.execute(query)
#             records = self.cursor.fetchall()
#             return records

    def addAccount(self, ownerName, owner_ssn, balance, account_status):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "insert into accounts (ownerName, owner_ssn, balance, account_status) values (%s, %s, %s, %s)" 
            values = (ownerName, owner_ssn, balance, "active")
            self.cursor.execute(query, values)
            self.connection.commit()
#             inserts a row into accounts %s and %d acts a placeholder for actual input 

#     def accountTransactions(self, accountID):
#         if self.connection.is_connected():
#             self.cursor = self.connection.cursor()
#             query = "select * from Transactions where accountID = %s"
#             values = (accountID)
#             self.cursor.execute(query, values)
#             records = self.cursor.fetchall()
#             return records

#     def deleteAccount(self, accountID):
#         if self.connection.is_connected():
#             self.cursor = self.connection.cursor()
#             query = "delete FROM accounts where accountId = %s"
#             values = (accountID)
#             self.cursor.execute(query, values)
#             self.connection.commit()
#           query = "delete from Transactions where accountID = %s" removes account in transactions


# In[ ]:


from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep


import cgi

class PortalRequestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = Database()
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_POST(self):
       
        try:
            if self.path == '/addAccount':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                ownerName = form.getvalue("oname")
                owner_ssn = int(form.getvalue("owner_ssn"))
                balance = float(form.getvalue("balance"))
                account_status = "active"
                self.database.addAccount(ownerName, owner_ssn, balance, account_status)

               
               

                print("Account Information",ownerName,owner_ssn,balance)
                
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<h3>Account have been added</h3>")
                self.wfile.write(b"<div><a href='/addAccount'>Add a New Account</a></div>")
                self.wfile.write(b"</center></body></html>")
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


        return


    def do_GET(self):
        try:
            if self.path == '/':
                
                data = []
                records = self.database.getAllAccounts()
                data = records
                print(records)
                
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>All Accounts</h2>")
                self.wfile.write(b"<table border=2>                                     <tr><th> Account ID </th>                                        <th> Account Owner</th>                                        <th> Balance </th>                                        <th> Status </th></tr>")
                for row in data:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return
            if self.path == '/addAccount':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Add New Account</h2>")

                self.wfile.write(b"<form action='/addAccount' method='post'>")
                self.wfile.write(b'<label for="oname">Owner Name:</label>                      <input type="text" id="oname" name="oname"><br><br>                      <label for="owner_ssn">Owner SSN:</label>                      <input type="number" id="owner_ssn" name="owner_ssn"><br><br>                      <label for="balance">Balance:</label>                      <input type="number" step="0.01" id="balance" name="balance"><br><br>                      <input type="submit" value="Submit">                      </form>')
                
                self.wfile.write(b"</center></body></html>")
                return
            if self.path == '/withdraw':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Withdraw from an account</h2>")

                self.wfile.write(b"</center></body></html>")
                return
            
            if self.path =='/deposit':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Deposit into an account</h2>")

                self.wfile.write(b"</center></body></html>")
                return
            if self.path =='/searchTransactions':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Results of your search</h2>")

                self.wfile.write(b"</center></body></html>")
                return


            if self.path =='/deleteAccount':
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title> Bank's Portal </title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Bank's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>|                                  <a href='/addAccount'>Add Account</a>|                                  <a href='/withdraw'>Withdraw</a>|                                  <a href='/deposit'>Deposit </a>|                                  <a href='/searchTransactions'>Search Transactions</a>|                                  <a href='/deletAccount'>Delete Account</a></div>")
                self.wfile.write(b"<hr><h2>Account has been deleted</h2>")

                self.wfile.write(b"</center></body></html>")
                return



        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

     
            
def run(server_class=HTTPServer, handler_class=PortalRequestHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()
    
run()


# In[ ]:



        
        
        

        
        


# In[ ]:





# In[ ]:





# In[ ]:



                


# In[ ]:



    
   


# In[ ]:




