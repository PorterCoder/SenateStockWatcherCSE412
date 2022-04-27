from cgitb import text
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import db

root = Tk()
root.title('Senate Stock Tracker Application')

t_list = Listbox(root)
selectedIndex = None
selectedTransaction = None
selectedRange = StringVar()
selectedType = StringVar()

addStock = StringVar()
addSenator = StringVar()
addType = StringVar()
addAmount = StringVar()
addDate = StringVar()

def openAddWdn():
    global addStock, addSenator, addType, addAmount, addDate
    #toplevel object which will be treated as a new window
    newWindow = Toplevel(root)

    #sets the title of the new window
    newWindow.title("Add Transaction Window")
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
    stkSelect = Entry(newWindow, textvariable=addStock, width=30)
    stkSelect.grid(row=1,column=1)
    senSelect = Entry(newWindow, textvariable=addSenator, width=30)
    senSelect.grid(row=2,column=1)
    stkType = Entry(newWindow, textvariable=addType, width=30)
    stkType.grid(row=3,column=1)
    amount = Entry(newWindow, textvariable=addAmount, width=30)
    amount.grid(row=4,column=1)
    date = Entry(newWindow, textvariable=addDate, width=30)
    date.grid(row=5, column=1)

    #create confirm button
    confirm_btn = Button(newWindow, text="confirm", command=confirm)
    confirm_btn.grid(row=6, column=1, columnspan=2,padx=10,pady=10,ipadx=100)


def confirm():
    stockName = addStock.get()
    senatorName = addSenator.get()
    stockType = addType.get()
    amount = addAmount.get()
    date = addDate.get()

    if not (stockName and senatorName and stockType and amount and date):
        messagebox.showerror(title="Add Transaction", message="Missing information.")
    else:
        senator_id = db.find_senator_id(senatorName)
        stock_id = db.find_stock_id(stockName)

        if not (senator_id and stock_id):
            messagebox.showerror(title="Add Transaction", message="Unable to find senator or stock id.")
        else:
            db.add_transaction(senator_id, stock_id, amount, date, stockType)
            addTransactionsToList()
            
def filterTransactions():
    if not selectedRange.get() or not selectedType.get():
        messagebox.showerror(title="Filter Transactions", message="No range or stock type selected.")
        addTransactionsToList()
    else:
        t = db.get_transactions_with_amount_range_and_type(selectedRange.get(), selectedType.get())
        addTransactionsToList(t)

def resetFilter():
    global selectedRange, selectedType
    selectedRange.set("")
    selectedType.set("")
    addTransactionsToList()

def addFilter():
    global selectedRange, selectedType
    
    ranges = ["$1,001 - $15,000", "$15,001 - $50,000", "$50,001 - $100,000", "$100,001 - $250,000", "$250,001 - $500,000", "$500,001 - $1,000,000"]
    AmountRange = OptionMenu(root, selectedRange, *ranges)
    AmountRange.grid(row=0, column=1)

    types = [t for types in db.get_stock_sectors() for t in types if t is not None]
    StockType = OptionMenu(root, selectedType, *types)
    StockType.grid(row=1, column=1)

    AmountRange_label = Label(root, text="Amount Range")
    AmountRange_label.grid(row=0, column=0)
    StockType_label = Label(root, text="Stock Type")
    StockType_label.grid(row=1, column=0)

    filter_btn = Button(root, text="Filter", command=filterTransactions)
    filter_btn.grid(row=2, column=1, columnspan=1, padx=10, pady=10, ipadx=100)

    reset_btn = Button(root, text="Reset", command=resetFilter)
    reset_btn.grid(row=2, column=0, columnspan=1, padx=10, pady=10, ipadx=100)


def addList():
    t_list.grid(row=3, column = 0,columnspan=2,padx=10,pady=10,ipadx=100, sticky=W + E)
    vbar = Scrollbar(t_list, orient="vertical")
    vbar.config(command=t_list.yview)
    t_list.config(yscrollcommand=vbar.set)
    t_list.bind("<<ListboxSelect>>", list_select)

def list_select(event):
    global selectedIndex, selectedTransaction
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        t_id = int(data.split(": ")[0].split(" ")[1])
        selectedIndex = index
        selectedTransaction = t_id

def addTransactionsToList(transactions=None):
    global t_list
    if transactions == None: transactions = db.get_all_transactions()
    t_list.delete(0, END)
    for t in transactions:
        t_message = "Transaction " + str(t[0]) + ": " + str(t[3]) + " | " + str(t[4]) + " | " + str(t[5])
        t_list.insert(END, t_message)

def deleteTransaction():
    global selectedIndex, selectedTransaction
    if not selectedTransaction:
        messagebox.showerror(title="Delete Transaction", message="No transaction currently selected.")
    else:
        deleted = db.delete_transaction(selectedTransaction)
        if deleted:
            t_list.delete(selectedIndex)
            messagebox.showinfo(title="Delete Transaction", message=f"Successfully deleted transaction {selectedTransaction}.")
            selectedIndex = None
            selectedTransaction = None
        else:
            messagebox.showerror(title="Delete Transaction", message=f"Unable to delete transaction {selectedTransaction}.")

def addButtons():
    #create add button
    add_btn = Button(root, text="Add Transaction", command=openAddWdn) #opens another widet
    add_btn.grid(row=4, column=0, padx=10, pady=10, ipadx=100)

    #create delete button
    delete_btn = Button(root, text="Delete Transaction", command=deleteTransaction)
    delete_btn.grid(row=4, column=1, padx=10, pady=10, ipadx=100)



def addAllElements():
    addFilter()

    addList()
    addTransactionsToList()

    addButtons()



db.start_connection()
addAllElements()
mainloop()
