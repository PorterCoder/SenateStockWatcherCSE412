from tkinter import *
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title('Senate Stock Watcher')
root.geometry("400x400")

#databases

#Create a database or connect to one
connect = sqlite3.connect('address_book.db') #connect a database

#create a cursor
cursor = connect.cursor()

#create table

# cursor.execute("""CREATE TABLE addresses (
#     first_name text, 
#     last_name text,
#     address text,
#     city text,
#     state text,
#     zipcode integer
#     )""")

#create function to delete a record
def delete():
    connect = sqlite3.connect('address_book.db') #connect a database

    #create a cursor
    cursor = connect.cursor()


    #Delete a record
    cursor.execute("DELETE from addresses WHERE oid=PLACEHOLDER")
    


        #commit changes
    connect.commit()

    #close connection
    connect.close()


#create sumbit function for database
def submit():

    #Create a database or connect to one
    connect = sqlite3.connect('address_book.db') #connect a database

    #create a cursor
    cursor = connect.cursor()

    #insert into table
    cursor.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
        {
            'f_name': f_name.get(),
            'l_name': l_name.get(),
            'address': address.get(),
            'city': city.get(),
            'state': state.get(),
            'zipcode': zipcode.get()
        }
    )

    #commit changes
    connect.commit()

    #close connection
    connect.close()


    #clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


#create query function
def query():
    #Create a database or connect to one
    connect = sqlite3.connect('address_book.db') #connect a database

    #create a cursor
    cursor = connect.cursor()

    #query the database
    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()
    #print(records)
    #loop thru results
    print_records = ''
    for record in records:
        print_records += str(record) + "\n"
        #record[0] will just print name

    query_label = Label(root, text=print_records)
    query_label.grid(row=8, column=0, columnspan=2)

    #commit changes
    connect.commit()

    #close connection
    connect.close()


#create text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0,column=1)

l_name = Entry(root, width=30)
l_name.grid(row=1,column=1)

address = Entry(root, width=30)
address.grid(row=2,column=1)

city = Entry(root, width=30)
city.grid(row=3,column=1)

state = Entry(root, width=30)
state.grid(row=4,column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5,column=1)


#create text box labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0)

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)

#Create submit button
submit_btn = Button(root, text="Add Record to Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


#create a query button
query_btn = Button(root, text="Show Records", command = query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)


#commit changes
connect.commit()

#close connection
connect.close()

root.mainloop()