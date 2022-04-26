from tkinter import *
from PIL import ImageTk, Image
import main
import sys

#GUI
root = Tk()
root.title('Senate Stock Tracker Application')
root.geometry("600x600")


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
filter_btn = Button(root, text="Filter!", command=get_transactions_in_amount_range())
filter_btn.grid(row=0, column=1, columnspan=2,padx=10,pady=10,ipadx=100)


#create a frame for the canvas with non-zero row and column
frame = Frame(root)
frame.grid(sticky='news')

#the canvas which supports the scrollbar interface, layout to the left
canvas = Canvas(frame, bg='#FFFFFF')
canvas.pack(side="left", fill="both", expand=True)

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
add_btn = Button(root, text="Add Transaction", command=add_transaction)
add_btn.grid(row=4, column=0,columnspan=1, padx=10,pady=10,ipadx=100)

#create filter button
delete_btn = Button(root, text="Delete Transaction", command=delete_transaction)
delete_btn.grid(row=4, column=1, columnspan=2, padx=10,pady=10,ipadx=100)








mainloop()