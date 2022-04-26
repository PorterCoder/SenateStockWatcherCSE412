import psycopg2
from tkinter import *
from PIL import ImageTk, Image

def connect_postgres(name, user, password):
    print("Attempting to connect to the database...")
    n = name
    u = user
    if u == "":
        u = "postgres"
    p = password
    c = None
    try:
        c = psycopg2.connect(
            dbname=n,
            user=u,
            host='localhost',  # assumes local host for now
            password=p
        )
        print("Successful Connection.")
    except Exception as err:
        print("I am unable to connect to the database")
        c = None
        exit()
    return c


def print_all_senators(senators):
    print("Printing all senators:")
    for senator in senators:
        print("   " + str(senator))  # print the senator row


def print_all_states(states):
    print("Printing all states:")
    for state in states:
        print("   " + str(state))  # print the states row


def print_all_transactions(transactions):
    print("Printing all states:")
    for transaction in transactions:
        print("   " + str(transaction))  # print the states row


# print transactions in a formatted style
def print_transactions(transactions):
    for transaction in transactions:
        print("Transaction " + str(transaction[0]) + ": " + str(transaction[3]) + " | " + str(
            transaction[4]) + " | " + str(transaction[5]))


def get_all_senators():
    cur.execute("SELECT * FROM senator")
    result = cur.fetchall()

    return result


def get_all_states():
    cur.execute("SELECT * FROM state")
    result = cur.fetchall()

    return result


def get_all_transactions():
    cur.execute("SELECT * FROM transaction")
    result = cur.fetchall()

    return result


# set value to less than or equal to 0 for any of the ranges to not check that range
def get_transactions_in_amount_range(amount_range):
    # amount_range == $1,001 - $15,000 or $50,001 - $100,000
    # or $15,001 - $50,000 or $100,001 - $250,000
    # or $250,001 - $500,000 or $500,001 - $1,000,000

    # sql query beforehand
    sql_query = "SELECT * FROM transaction WHERE t_amount = '" + amount_range + "'"
    cur.execute(sql_query)
    result = cur.fetchall()

    print(sql_query)

    # return the result
    return result


def get_transactions_with_type(transaction_type):
    # sql query beforehand
    sql_query = "SELECT * FROM transaction WHERE t_type = '" + transaction_type + "'"
    cur.execute(sql_query)
    result = cur.fetchall()

    print(sql_query)

    # return the result
    return result


def sort_transaction_by_column(transactions, column_index, is_reversed):
    print("attempting to sort by column: " + str(column_index))
    result = transactions

    # if this list is empty then return
    if not transactions:
        print("the transaction list you are trying to sort is empty!")
        return

    # if the column to sort by is not in range then return
    if column_index not in range(0, len(transactions[0])):
        print(str(column_index) + " is not in range of 0 - " + str(len(transactions[0]) - 1))
        return

    # sort by the column index
    result.sort(key=lambda i: i[column_index], reverse=is_reversed)

    print("sorting transaction by column " + str(column_index) + " was successful!")
    return result


def add_transaction(senator_id, stock_id, amount_range, date, stock_type):
    # get all the transactions
    transactions = get_all_transactions()

    # get the last transaction in the list sorted by ids, make this transaction id + 1 that
    # most recent transaction should be the first
    result = sort_transaction_by_column(transactions, 0, True)
    print(result)

    # get the first id in transaction list
    new_id = int(result[0][0]) + 1

    print("adding new transaction with id of " + str(new_id))

    sql_query = "INSERT INTO transaction(t_transactionid, t_senatoridkey, t_stockidkey, t_amount, t_date, t_type) VALUES"
    sql_query += " ('" + str(new_id) + "', '" + str(senator_id) + "', '" + str(stock_id) + "', '" + str(amount_range)
    sql_query += "', '" + str(date) + "', '" + str(stock_type) + "')"
    print(sql_query)
    cur.execute(sql_query)


def delete_transaction(transaction_id):
    transactions = get_all_transactions()
    removed = []
    for transaction in transactions:
        if int(transaction[0]) == transaction_id:
            print("found id of: " + str(transaction_id))
            removed = transaction
            print("removing...")
            cur.execute("DELETE FROM transaction WHERE t_transactionid = '" + str(transaction_id) + "'")
            print("removed")
            break

    # if removed is null then could not find
    if not removed:
        print("could not find transaction of id: " + str(transaction_id))
    else:
        print("removed transaction: " + str(transaction))


#GUI
root = Tk()
root.title('Senate Stock Tracker Application')
root.geometry("600x600")


def openAddWdn():
    #toplevel object which will be treated as a new window
    newWindow = Toplevel(root)

    #sets the title of the new window
    newWindow.title("Add Transaction Window")
    newWindow.geometry("600x600")
    title_label = Label(newWindow, text="Automatically Assign New Transaction ID")
    title_label.grid(row=0, column=0, columnspan=2)

    stkSelect_label = Label(newWindow, text="Stock Selection: ")
    stkSelect_label.grid(row=1,column=0)
    senSelect_label = Label(newWindow, text="Senator Selection: ")
    senSelect_label.grid(row=2,column=0)
    stkType_label = Label(newWindow, text="Stock Type (Buy/Sale): ")
    stkType_label.grid(row=3,column=0)
    amount_label = Label(newWindow, text="Amount: ")
    amount_label.grid(row=4,column=0)
    date_label = Label(newWindow, text="Date: ")
    date_label.grid(row=5,column=0)

    #create text boxes
    stkSelect = Entry(newWindow, width=30)
    stkSelect.grid(row=1,column=1)
    senSelect = Entry(newWindow, width=30)
    senSelect.grid(row=2,column=1)
    stkType = Entry(newWindow, width=30)
    stkType.grid(row=3,column=1)
    amount = Entry(newWindow, width=30)
    amount.grid(row=4,column=1)
    date = Entry(newWindow, width=30)
    date.grid(row=5, column=1)

    #create confirm button
    confirm_btn = Button(newWindow, text="confirm", command=add_transaction)
    confirm_btn.grid(row=6, column=1, columnspan=2,padx=10,pady=10,ipadx=100)





#create text boxes
AmountRange = Entry(root, width=30)
AmountRange.grid(row=1,column=1)
StockType = Entry(root, width=30)
StockType.grid(row=2,column=1)

#create text label
filter_label = Label(root, text="Filter Options")
filter_label.grid(row=0,column=0)
AmountRange_label = Label(root, text="Amount Range")
AmountRange_label.grid(row=1, column=0)
StockType_label = Label(root , text="Stock Type")
StockType_label.grid(row=2, column=0)

#create filter button
filter_btn = Button(root, text="Filter!", command=get_transactions_in_amount_range)
filter_btn.grid(row=0, column=1, columnspan=2,padx=10,pady=10,ipadx=100)


#create a frame for the canvas with non-zero row and column
frame = Frame(root)
frame.grid(sticky='news')

#the canvas which supports the scrollbar interface, layout to the left
canvas = Canvas(frame, bg='#FFFFFF')
canvas.pack(side="left", fill= X, expand=True)


#the scrollbar, layout to the right
vbar=Scrollbar(frame,orient=VERTICAL, command=canvas.yview)
vbar.pack(side="right",fill="y")

#bind the scrollbar to the cavas
canvas.configure(yscrollcommand=vbar.set)
vbar.configure(command=canvas.yview)

# The Frame to be scrolled, layout into the canvas
# All widgets to be scrolled have to use this Frame as parent
scrolled_frame = Frame(canvas, background=canvas.cget('bg'))
canvas.create_window((4, 4), window=scrolled_frame, anchor="nw")


#create filter button
add_btn = Button(root, text="Add Transaction", command=openAddWdn) #opens another widet
add_btn.grid(row=4, column=0,columnspan=1, padx=10,pady=10,ipadx=100)

#create filter button
delete_btn = Button(root, text="Delete Transaction", command=delete_transaction) #shuld delete
delete_btn.grid(row=4, column=1, columnspan=2, padx=10,pady=10,ipadx=100)


mainloop()


databaseName = input("enter the database name: ")
databaseUser = input("enter your database username: (blank for default)")
databasePassword = input("enter your database password: ")

conn = connect_postgres(databaseName, databaseUser, databasePassword)
cur = conn.cursor()




# EXAMPLES -----------------------------------------------------------------------------------------------------

# add a transaction with all this information using transaction id of the largest id + 1
add_transaction(1, 1, "$1,000-2,5000", "2022-03-03", "Purchase")

# get all transactions, sort, and print
print_transactions(sort_transaction_by_column(get_all_transactions(), 0, True))

# try to delete the transaction with id of 479 (should be newest one)
delete_transaction(479)

# get all transactions, sort, and print
print_transactions(sort_transaction_by_column(get_all_transactions(), 0, True))

# test = get_transactions_in_amount_range("$1,001 - $15,000")

# sort by transaction result by id (transaction 1 first when True, the newest transaction first when False)
# sorted_by_id = sort_transaction_by_column(test, 0, True)
# sort by transaction result by date (the newest first when True, oldest when False)
# sorted_by_date = sort_transaction_by_column(test, 4, True)

# print_transactions(sorted_by_id)
# print_transactions(sorted_by_date)
