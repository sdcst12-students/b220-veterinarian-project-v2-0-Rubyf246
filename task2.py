import sqlite3

##################### class definition
class Vet:
    def __init__(self, myDB):
        # class attributes
        self.myDB = myDB  #database name
        self.connection = None
        self.cursor = None
        self.connect()
        
    def connect(self): #class method, connect to database
        try:
            self.connection = sqlite3.connect(self.myDB)
            self.cursor = self.connection.cursor()
            print(f"Connected to {self.myDB} successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database {self.myDB} : {e}")

    def close_conn(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")

    def exec_query(self, query, params=()):  #class method, execute query
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query {query}: {e}")
            return None
         
    
        
    def create_customers_table(self):  #class method, create table customers
        query_drop_tbl = "drop table if exists customers"
        self.exec_query(query_drop_tbl)
        query_create_tbl = """create table if not exists customers 
            ( 
            id integer primary key autoincrement, 
            fname tinytext, 
            lname tinytext,
            phone int, 
            email tinytext,
            address tinytext,
            city tinytext,
            postalcode tinytext
            );"""
        self.exec_query(query_create_tbl)  
        print(f"Created customers table.")
        
    def create_visits_table(self): #class method, create table visits
        query_drop_tbl = "drop table if exists visits"
        self.exec_query(query_drop_tbl)
        query_create_tbl = """create table visits 
        ( 
            id integer primary key autoincrement,
            ownerID int,
            petid int,
            details tinytext,
            cost int,
            paid int
        ); 
        """
        self.exec_query(query_create_tbl)  
        print(f"Created visits table.")
        
    def create_pets_table(self):  #class method, create table pets
        query_drop_tbl = "drop table if exists pets"
        self.exec_query(query_drop_tbl)
        query_create_tbl =  """create table pets 
        ( 
            id integer primary key autoincrement, 
            name tinytext,
            type tinytext,
            breed tinytext,
            birthdate tinytext,
            ownerID int
        ); 
        """
        self.exec_query(query_create_tbl)   
        print(f"Created pets table.")        



    def search(self, myTable, myfilter): #class method, select from a table
        query = f"SELECT * FROM {myTable}"
        if myfilter != '':
            query += f" WHERE {myfilter}"
            print (query) 
        return self.exec_query(query)

    
    
    def insert(self, myTable, data):
        if myTable == "customers":
            for i in data:
                query_insert = f"insert into customers (fname, lname, phone, email,  address, city, postalcode) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}','{i[5]}','{i[6]}');"
                self.exec_query(query_insert) 
        if myTable == "pets":
            for i in data:
                query_insert = f"insert into pets (name, type, breed, birthdate, ownerID) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}');"
                self.exec_query(query_insert) 
        if myTable == "visits":        
            for i in data:
                query_insert = f"insert into visits (ownerID, petid, details, cost, paid) values ('{i[0]}','{i[1]}','{i[2]}','{i[3]}','{i[4]}');"
                self.exec_query(query_insert) 
        
        
            
        
    def update(self, myTable, myCol, newVal, myfilter):
        query_update = f"update {myTable} set {myCol} = '{newVal}'  WHERE {myfilter}"
        print ("--- upd qry")
        print (query_update)
        self.exec_query(query_update) 

    def delete(self, myTable, myfilter):
        query_del = f"DELETE FROM {myTable} WHERE {myfilter}"
        self.exec_query(query_del)
    
    def say_hi(self):
        print('Hello, my database name is', self.myDB)    
        
        
################################## TEST ##############################################

########## Create tables
myVet = Vet("Veterinarian") # initialize an object of class Vet
myVet.say_hi()   
myVet.create_customers_table()
myVet.create_visits_table()
myVet.create_pets_table()

########## Insert data to customers table
cust_data = [
('Jen', 'Mezei', '6042231134', 'jen@shaw.ca',  '891 Cullen Cresc', 'Delta', 'V4L1Q2'),
('John', 'Shu', '6042232255', 'js@shaw.ca',  '123 Dan Rd', 'Surrey', 'V4N1C8'),
('Mary', 'Shu', '6042232255', 'ms@shaw.ca',  '123 Dan Rd', 'Surrey', 'V4N1C8')
]

myVet.insert( "customers", cust_data)
result = myVet.search("customers","")     #check customers data
print ("data in table customers after insert:")
print ("--------------------------------------")
for i in result:
    print(i)


########## Insert data to pets table
pets_data = [
('Casey', 'Cat', 'Persion', '2024-10-02', 1),
('Maggie', 'Cat', 'BritishShortHair', '2023-01-12', 2),
('Ben', 'Dog', 'Lab', '2024-10-02', 1),
('Tina', 'Dog', 'Lab', '2023-01-12', 2)
]

myVet.insert( "pets", pets_data)
result = myVet.search("pets", "")     #check customers data
print ("\ndata in table pets after insert:")
print ("--------------------------------------")
for i in result:
    print(i)
    
########## Insert data to visits table
visits_data = [
(1, 1, 'grooming', 23, 20),
(2, 2, 'washing', 50, 50),
(2, 2, 'washing', 50, 50)
]

myVet.insert( "visits", visits_data)
result = myVet.search("visits","")     #check customers data
print ("\ndata in table visits after insert:")
print ("--------------------------------------")
for i in result:
    print(i)    
    
########## Update data to pets table    
myVet.update("pets", "type", "Dog", "  id = 2")
 
result = myVet.search("pets", "") 
print ("\ndata in table pets after update:")
print ("--------------------------------------")
for i in result:
    print(i)  
    
########## delete data from visits table     
#myVet.delete("visits", " id = 1 ") 
#result = myVet.search("visits","")     #check customers data
#print ("\ndata in table visits after delete:")
#print ("--------------------------------------")
#for i in result:
#    print(i) 

def search_customer():
    customer_col_dictionary = {
        "1":"id", 
        "2":"fname", 
        "3":"lname",
        "4":"phone", 
        "5":"email",
        "6":"city",
        "7":"address",
        "8":"postalcode" 
    }
    while (True):
            # ask the user what category they want to search by and out it into field 
            search_by = input ("What do you want to search by: \n1.id\n2.first name\n3.last name\n4.phone number\n5.email\n6.city\n7.address\n8.postal code\n9.exit\n ")
           
            if search_by not in ("1","2","3","4","5","6","7","8","9"):
                print ("Invalid entry search. Please choose option 1 to 9")
            if  search_by == "9":
                break   
            else:
                # ask the user what category they want to search by and out it into value
                search_by_value = input ("what is your value you want to search by:    ").replace(" ", "") 
                customer_filter =  (customer_col_dictionary[search_by]) + "='" + search_by_value + "'"
                result = myVet.search("customers", customer_filter)     #check customers data
            
                print ("\n" + str(len(result)) + " rows found in table customers with " + customer_filter + ":")
                print ("--------------------------------------")
                for i in result:
                    print(i)
                    
                    

    
def search_pet():
    pet_col_dictionary = {
        "1": "name",
        "2": "type",
        "3": "breed",
        "4": "birthdate",
        "5": "ownerID"
    }
    while (True):
            # ask the user what category they want to search by and out it into field 
            search_by = input ("What do you want to search by: \n1.name\n2.type\n3.breed\n4.birthdate\n5.ownerID\n6.exit\n ")
           
            if search_by not in ("1","2","3","4","5","6"):
                print ("Invalid entry search. Please choose option 1 to 6")
            if  search_by == "6":
                break   
            else:
                # ask the user what category they want to search by and out it into value
                search_by_value = input ("what is your value you want to search by:    ").replace(" ", "") 
                pet_filter =  (pet_col_dictionary[search_by]) + "='" + search_by_value + "'"
                result = myVet.search("pets", pet_filter)     #check customers data
            
                print ("\n" + str(len(result)) + " rows found in table pets with " + pet_filter + ":")
                print ("--------------------------------------")
                for i in result:
                    print(i)    
        
def search_visit():
    visit_col_dictionary = {
        "1":"id", 
        "2":"ownerID", 
        "3":"petid",
        "4":"details", 
        "5":"cost",
        "6":"paid",
       
    }
    while (True):
            # ask the user what category they want to search by and out it into field 
            search_by = input ("What do you want to search by: \n1.id\n2.ownerID\n3.petid\n4.details\n5.cost\n6.paid\n7.exit\n ")
           
            if search_by not in ("1","2","3","4","5","6","7"):
                print ("Invalid entry search. Please choose option 1 to 7")
            if  search_by == "7":
                break   
            else:
                # ask the user what category they want to search by and out it into value
                search_by_value = input ("what is your value you want to search by:    ").replace(" ", "") 
                filter =  (visit_col_dictionary[search_by]) + "='" + search_by_value + "'"
                result = myVet.search("visits", filter)     #check customers data
            
                print ("\n" + str(len(result)) + " rows found in table customers with " + filter + ":")
                print ("--------------------------------------")
                for i in result:
                    print(i)        

def insert_customer():
    print ("\n----------------Add a customer :------------------");    
    inpt_fname = input("Enter first name: ")
    inpt_lname = input("Enter last name: ")
    inpt_ph = input("Enter phone: ")
    inpt_email = input("Enter email: ")
    inpt_addr = input("Enter address: ")
    inpt_city = input("Enter city: ")
    inpt_pcode = input("Enter postal code: ")
    cust_data = [
                (inpt_fname, inpt_lname, inpt_ph, inpt_email,  inpt_addr, inpt_city, inpt_pcode)
        ]

    myVet.insert( "customers", cust_data)

def update_customer():
    inpt_id = int(input("Enter ID of the customer you want to update: "))
    updatechoice= input(" Choose: \n1: change first name  \n2: change last name  \n3: change phone number \n4: change email \n5: change address \n6: change city \n7: change postal code \n")
    if updatechoice not in ("1","2","3","4","5","6","7"):
        print ("Invalid choice. Please choose option 1 to 7")
    else:
        col_dictionary = {
            "1":"fname", 
            "2":"lname",
            "3":"phone", 
            "4":"email",
            "5":"city",
            "6":"address",
            "7":"postalcode" 
        }
        new_value = input( " Please enter new value of " + col_dictionary[updatechoice] + ":")
        myVet.update("customers", col_dictionary[updatechoice], new_value, "  id = " + str(inpt_id))

    
            
        
def insert_pet():
        print ("\n----------------Add a pet :------------------");    
        inpt_name = input("Enter name: ")
        inpt_type = input("Enter type: ")
        inpt_breed = input("Enter breed: ")
        inpt_bdate = input("Enter birthdate (yyyy-MM-dd): ")
        inpt_ownerID = input("Enter ownerID: ")
        pet_data = [(inpt_name, inpt_type, inpt_breed, inpt_bdate, int(inpt_ownerID))]  
        myVet.insert( "pets", pet_data)     
        
def update_pet():
    inpt_id = int(input("Enter ID of the pet you want to update: "))
    updatechoice= input(" Choose: \n1: change pet name  \n2: change pet type  \n3: change pet breed \n4: change pet birthday (yyyy-MM-dd) \n5: change ownerID \n")
    if updatechoice not in ("1","2","3","4","5"):
        print ("Invalid choice. Please choose option 1 to 5")
    else:
        col_dictionary = {
            "1":"name", 
            "2":"type",
            "3":"breed", 
            "4":"birthday",
            "5":"ownerID" 
        }
        new_value = input( " Please enter new value of " + col_dictionary[updatechoice] + ":")
        myVet.update("pets", col_dictionary[updatechoice], new_value, "  id = " + str(inpt_id))
        
        
 
def insert_visit():
        print ("\n----------------Add a visit :------------------");  
        
           
        ownerID = input("Enter ownerID: ")
        petid = input("Enter petid: ")
        details = input("Enter details: ")
        cost = input("Enter cost: ")
        paid = input("Enter paid: ")
        visit_data = [(ownerID, petid, details, int(cost), int(paid))]  
        myVet.insert( "visits", visit_data)    
     
     
def update_visit():
    inpt_id = int(input("Enter ID of the visit you want to update: "))
    updatechoice= input(" Choose: \n1: change ownerID  \n2: change pet ID  \n3: change details of the visit \n4: change cost (dollars) \n5: change paid amount (dollars) \n")
    if updatechoice not in ("1","2","3","4","5"):
        print ("Invalid choice. Please choose option 1 to 5")
    else:
        visit_col_dictionary = {
        "1":"ownerID", 
        "2":"petid",
        "3":"details", 
        "4":"cost",
        "5":"paid"}
        new_value = input( " Please enter new value of " + visit_col_dictionary[updatechoice] + ":")
        myVet.update("visits", visit_col_dictionary[updatechoice], new_value, "  id = " + str(inpt_id))

 

########### starting user interface
while (True):
    #operation = input("Input your operation (search/add/update/exit) ---->    ").lower().replace(" ", "")
    operation = input("Please choose operation: \n1.search\n2.add\n3.update\n4.exit\n ").replace(" ", "")
    if operation == "1": 
        while (True):
            # ask the user what category they want to search by and out it into field 
            search_tbl = input ("Which table to you want to search: \n1.customers\n2.pets\n3.visits\n4.exit\n ")
            if search_tbl not in ("1","2","3","4"):
                print ("Invalid entry search. Please choose option 1 to 4")
            elif search_tbl == "4":
                break
            elif search_tbl == "1":
                search_customer()
            elif search_tbl == "2":
                search_pet()
            elif search_tbl == "3":
                search_visit()    
                    
                   
    elif operation == "2":
        #################  Add a new customer ###################
         insert_tbl = input ("Which table to you want to insert: \n1.customers\n2.pets\n3.visits\n4.exit\n ")
         if insert_tbl not in ("1","2","3","4"):
                print ("Invalid entry search. Please choose option 1 to 4")
         elif insert_tbl == "4":
                break
         elif insert_tbl == "1":
                insert_customer()
         elif insert_tbl == "2":
                insert_pet()
         elif insert_tbl == "3":
                insert_visit()
        
        
    elif operation == "3":
         update_tbl = input ("Which table to you want to update: \n1.customers\n2.pets\n3.visits\n4.exit\n ")
         if update_tbl not in ("1","2","3","4"):
                print ("Invalid entry. Please choose option 1 to 4")
         elif update_tbl == "4":
                break
         elif update_tbl == "1":
                update_customer()
         elif update_tbl == "2":
                update_pet()
         elif update_tbl == "3":
                update_visit()
              
    elif operation == "4":
        break
    else: 
        print("invalid response, please enter one of the four operations: 1 for search, 2 for add, 3 for update or 4 for exit")        
        
