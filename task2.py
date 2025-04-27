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



    def select(self, myTable, myfilter): #class method, select from a table
        query = f"SELECT * FROM {myTable}"
        if myfilter != '':
            query += f" WHERE {myfilter}"
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
('John', 'Shu', '6042232255', 'js@shaw.ca',  '123 Dan Rd', 'Surrey', 'V4N1C8')
]

myVet.insert( "customers", cust_data)
result = myVet.select("customers","")     #check customers data
print ("data in table customers after insert:")
print ("--------------------------------------")
for i in result:
    print(i)


########## Insert data to pets table
pets_data = [
('Casey', 'Cat', 'Persion', '2024-10-02', 1),
('Maggie', 'Cat', 'Lab', '2023-01-12', 2)
]

myVet.insert( "pets", pets_data)
result = myVet.select("pets", "")     #check customers data
print ("\ndata in table pets after insert:")
print ("--------------------------------------")
for i in result:
    print(i)
    
########## Insert data to visits table
visits_data = [
(1, 1, 'grooming', 23, 20),
(2, 2, 'washing', 50, 50)
]

myVet.insert( "visits", visits_data)
result = myVet.select("visits","")     #check customers data
print ("\ndata in table visits after insert:")
print ("--------------------------------------")
for i in result:
    print(i)    
    
########## Update data to pets table    
myVet.update("pets", "type", "Dog", "  id = 2")
 
result = myVet.select("pets", "") 
print ("\ndata in table pets after update:")
print ("--------------------------------------")
for i in result:
    print(i)  
    
########## delete data from visits table     
myVet.delete("visits", " id = 1 ") 
result = myVet.select("visits","")     #check customers data
print ("\ndata in table visits after delete:")
print ("--------------------------------------")
for i in result:
    print(i) 
    