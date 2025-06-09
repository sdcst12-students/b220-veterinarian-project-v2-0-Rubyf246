import sqlite3

file = 'dbase.db'
connection = sqlite3.connect(file)
print(connection)

cursor = connection.cursor()
query = "select sqlite_version();"

query = "drop table if exists customers"
cursor.execute(query)

query = "drop table if exists pets"
cursor.execute(query)

query = "drop table if exists visits"
cursor.execute(query)

###################### customers ###########################
query = """create table customers 
( 
id integer primary key autoincrement, 
fname tinytext, 
lname tinytext,
phone int, 
email tinytext,
address tinytext,
city tinytext,
postalcode tinytext
); 
"""
cursor.execute(query)

data = [
('Jen', 'Mezei', '6042231134', 'jen@shaw.ca',  '891 Cullen Cresc', 'Delta', 'V4L1Q2'),
('John', 'Shu', '6042232255', 'js@shaw.ca',  '123 Dan Rd', 'Surrey', 'V4N1C8')
]

for i in data:
    query = f"insert into customers (fname, lname, phone, email,  address, city, postalcode) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}','{i[5]}','{i[6]}');"
    cursor.execute(query)

connection.commit()
query = "select * from customers"
cursor.execute(query)
result = cursor.fetchall()


print ("----------------Initial Customers:------------------");

for i in result:
    print(i)

###################### pets ###########################
query = """create table pets 
( 
    id integer primary key autoincrement, 
    name tinytext,
    type tinytext,
    breed tinytext,
    birthdate tinytext,
    ownerID int
); 
"""
cursor.execute(query)

data = [
('Casey', 'Cat', 'Persion', '2024-10-02', 1),
('Holly', 'Cat', 'Tabby', '2023-01-12', 2)
]

for i in data:
    query = f"insert into pets (name, type, breed, birthdate, ownerID) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}');"
    cursor.execute(query)

connection.commit()
query = "select * from pets"
cursor.execute(query)
result = cursor.fetchall()

print ("----------------Initial Pets:------------------");

for i in result:
    print(i)

###################### visits ###########################
query = """create table visits 
( 
    id integer primary key autoincrement,
    ownerID int,
    petid int,
    details tinytext,
    cost int,
    paid int
); 
"""
cursor.execute(query)

data = [
(1, 1, 'grooming', 23, 20),
(2, 2, 'washing', 50, 50)
]

for i in data:
    query = f"insert into visits (ownerID, petid, details, cost, paid) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}');"
    cursor.execute(query)

connection.commit()
query = "select * from visits"
cursor.execute(query)
result = cursor.fetchall()

print ("----------------Initial Visits:------------------");
for i in result:
    print(i)



def insert_customer (fname, lname, ph, email, addr, city, pcode):
    cur = connection.cursor()
    cur.execute("insert into customers (fname, lname, phone, email,  address, city, postalcode) values (?,?,?,?,?,?,?);", (fname, lname, ph, email, addr, city, pcode))
    connection.commit()

##################  Search by email ###################   
#
###def search_customer_by_email (email): 
##    cursor = connection.cursor()
##    query = """select * from customers where email = ?"""
##    cursor.execute(query, (email,))
##    records = cursor.fetchall()
##    print("Search by email:  ", email)
##    for row in records:
##        print("First Name = ", row[1])
##        print("Last Name  = ", row[2])
##    cursor.close()
#    
def search_customer (search_field, search_by_value):
    ## decide what query is, based on search field
    
    if search_field == "email":
        query = """select * from customers where email = ?"""
    elif search_field == "first name":
        query = """select * from customers where fname = ?"""
    elif search_field == "last name":
        query = """select * from customers where lname = ?"""
    elif search_field == "phone number":
        query = """select * from customers where phone = ?"""    
    elif search_field == "email":
        query = """select * from customers where email = ?"""        
    elif search_field == "address":
        query = """select * from customers where address = ?"""        
    elif search_field == "city":
        query = """select * from customers where city = ?"""        
    elif search_field == "postal code":
        query = """select * from customers where postalcode = ?"""  
    elif search_field == "id":
        query = """select * from customers where id = ?"""           

    cursor = connection.cursor()
    cursor.execute(query, (search_by_value,))
    records = cursor.fetchall()
    print(f"Search by {search_field}:  ", search_by_value)
    for row in records:
        print("ID = ", row[0])
        print("First Name = ", row[1])
        print("Last Name  = ", row[2])
        print("Phone = ", row[3])
        print("Email  = ", row[4])
        print("Address = ", row[5])
        print("City  = ", row[6])
        print("Postal Code  = ", row[7])
    cursor.close()

###################  Ask which function they want to excute  ################

choice = input("Input your choice (search/add/update) ---->    ").lower().replace(" ", "")
if choice == "search":
    field = input ("What do you want to search by:    ") # ask the user what category they want to search by and out it into field 
    if field not in ("id", "first name", "last name", "phone number", "email", "city", "address", "postal code"):
        print ("Invalid entry search. Try again")
    else:
        # ask the user what category they want to search by and out it into value
        value = input ("what is your value you want to search by:    ") 
        search_customer (field,value)
        
if choice == "add":
   #################  Add a new customer ###################
    print ("\n----------------Add a customer :------------------");    
    inpt_fname = input("Enter first name: ")
    inpt_lname = input("Enter last name: ")
    inpt_ph = input("Enter phone: ")
    inpt_email = input("Enter email: ")
    inpt_addr = input("Enter address: ")
    inpt_city = input("Enter city: ")
    inpt_pcode = input("Enter postal code: ")
    insert_customer(inpt_fname,inpt_lname, inpt_ph ,inpt_email, inpt_addr,inpt_city,inpt_pcode)
    print ("\n----------------After Adding New Customer:------------------")
    #displays info after inserts
    query = "select * from customers"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        print(i)                                                                              

if choice=="update":
    updatechoice= input(" Choose: A: change first name  B: change last name  C: change phone number D: change email \n E: change address F: change city G: change postal code \n H: update information ")
    if updatechoice == "A":
        custoid= input(" What is the id you want to change? ---->  ")
        newfname= input("What is the first name you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET fname = ? 
                WHERE id = ?;'''
        #print (query)
        ## execute query
        cursor.execute(query, (newfname, custoid,))
                
    elif updatechoice =="B":
        custoid= input(" What is the id you want to change? ---->  ")
        newlname= input("What is the last name you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET lname = ?
                WHERE id = ?;'''
        cursor.execute(query, (newlname, custoid,))
        
    elif updatechoice =="C":
        custoid= input(" What is the id you want to change? ---->  ")
        newphone= input("What is the phone number you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET phone = ?
                WHERE id = ?;'''
        cursor.execute(query, (newphone, custoid,))
        
    elif updatechoice == "D":
        custoid= input(" What is the id you want to change? ---->  ")
        newemail= input("What is the email you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET email = ?
                WHERE id = ?;'''
        cursor.execute(query, (newemail, custoid,))
        
    elif updatechoice =="E":
        custoid= input(" What is the id you want to change? ---->  ")
        newaddress= input("What is the address you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET address = ?
                WHERE id = ?;'''
        cursor.execute(query, (newaddress, custoid,))
        
    elif updatechoice == "F":
        custoid= input(" What is the id you want to change? ---->  ")
        newcity= input("What is the city you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET city = ?
                WHERE id = ?;'''
        cursor.execute(query, (newcity, custoid,))
        
    elif updatechoice == "G": 
        custoid= input(" What is the id you want to change? ---->  ")
        newpostalcode= input("What is the postal code you want to replace it with?---->  ")
        query= '''UPDATE customers
                SET postalcode = ?
                WHERE id = ?;'''
        cursor.execute(query, (newpostalcode, custoid,))
        
    elif updatechoice == "H":
        query = '''SELECT * FROM Customers;'''

    connection.commit()   

    ## display updated customer info
    query = """select * from customers where id = ?"""  
    cursor.execute(query, (custoid,))  
    result = cursor.fetchall()


    print ("----------------display updated customer info:------------------");

    for i in result:
        print(i)
else: 
    print("invalid response")