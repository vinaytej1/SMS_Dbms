# import all the modules
from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox
import datetime
import os
import random
import re


DB_path = os.getcwd() + "\\Database\\store.db"

conn = sqlite3.connect(DB_path)
c = conn.cursor()

# date
date = datetime.datetime.now().date()

def show_frame(frame):
    frame.tkraise()


root = Tk()
root.geometry("1366x768+0+0")
root.title("General Store management System")
root.resizable(width=False, height=False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


frame1 = tkinter.Frame(root)
frame2 = tkinter.Frame(root)
frame3 = tkinter.Frame(root)
frame4 = tkinter.Frame(root, bg="grey")

for frame in (frame1, frame2, frame3, frame4):
    frame.grid(row=0, column=0, sticky='nsew')


products_list = []
product_price = []
product_quantity = []
product_id = []

labels_list = []




def change_func():

    global c_amount
    c_amount.configure(text="")

    amount_given = float(change_e.get())
    our_total = float(sum(product_price))

    to_give = amount_given - our_total

    p = "Change: Rs. " + str(to_give)
   
    c_amount = Label(left, text=p,
                     font=('arial 18 bold'), fg='red', bg='floral white')
    c_amount.place(x=0, y=600)


def ajax():
    global get_id, get_name, get_price, get_stock
    get_id = enteride.get()
    get_price = "NA"
    get_name = "Does not exist"

    # get the products info with that id and fill it in the labels above
    query = "SELECT * FROM inventory WHERE id=?"
    result = c.execute(query, (get_id, ))
    for r in result:
        get_id = r[0]
        get_name = r[1]
        get_price = r[4]
        get_stock = r[2]
    productname.configure(
        text="Product's Name: " + str(get_name))
    pprice.configure(text="Price: Rs. " + str(get_price))


def add_to_cart():
    # get the quantity value and from the database
    quantity_value = int(quantity_e.get())
    if quantity_value > int(get_stock):
        tkinter.messagebox.showinfo(
            "Error", "Not that many products in our inventory.")
    else:
        # calculate the price
        final_price = (float(quantity_value) * float(get_price)
                       ) - (float(discount_e.get()))

        products_list.append(get_name)
        product_price.append(final_price)
        product_quantity.append(quantity_value)
        product_id.append(get_id)

        x_index = 0
        y_index = 100
        counter = 0
        for p in products_list:
            tempname = Label(right, text=str(products_list[counter]), font=(
                'arial 18 bold'), bg='orange', fg='white')
            tempname.place(x=0, y=y_index)
            labels_list.append(tempname)

            tempqt = Label(right, text=str(product_quantity[counter]), font=(
                'arial 18 bold'), bg='orange', fg='white')
            tempqt.place(x=300, y=y_index)
            labels_list.append(tempqt)

            tempprice = Label(right, text=str(
                product_price[counter]), font=('arial 18 bold'), bg='orange', fg='white')
            tempprice.place(x=500, y=y_index)
            labels_list.append(tempprice)

            y_index += 40
            counter += 1

            # total configure
            total_l.configure(
                text="Total: Rs." + str(sum(product_price)))

            # delete
            productname.configure(text="")
            pprice.configure(text="")

            # Removes all the previous entries
            enteride.focus()
            enteride.delete(0, END)


def generate_bill():
    # create the bill before updating to the database.
    currentDirectory = os.getcwd()
    directory = currentDirectory + "\\Bills\\" + str(date) + "\\"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # TEMPLATES FOR THE BILL
    company = "\t\t\t\tTej Enterprise Pvt. Ltd.\n"
    address = "\t\t\t\tChickballapur, India\n"
    phone = "\t\t\t\t\t989758759988\n"
    sample = "\t\t\t\t\tInvoice\n"
    dt = "\t\t\t\t\t" + str(date)

    tresult = c.execute("SELECT Max(id) from transactions")
    for r in tresult:
        tid = r[0]
    bill_num = "\n\n\t\t\t" + "Bill number : " + str(tid)

    table_header = "\n\n\t\t\t---------------------------------------\n\t\t\tSN.\tProducts\t\tQty\t\tAmount\n\t\t\t---------------------------------------"
    final = company + address + phone + sample + dt + bill_num + "\n" + table_header

    # open a file to write it to
    file_name = str(directory) + \
        str(tid) + ".rtf"
    f = open(file_name, 'w')
    f.write(final)

    # fill dynamics
    r = 1
    i = 0
    for t in products_list:
        f.write("\n\t\t\t" + str(r) + "\t" + str(products_list[i] + ".......")[
                :7] + "\t\t" + str(product_quantity[i]) + "\t\t" + str(product_price[i]))
        i += 1
        r += 1
    f.write("\n\n\t\t\tTotal: Rs. " + str(sum(product_price)))
    f.write("\n\t\t\tThanks for Visiting.")
    os.startfile(file_name, "print")
    
    f.close()
    # decrease the stock
    x = 0

    initial = "SELECT * FROM inventory WHERE id=?"
    result = c.execute(initial, (product_id[x], ))

    for i in products_list:
        for r in result:
            old_stock = r[2]
        new_stock = int(old_stock) - \
            int(product_quantity[x])

        # updating the stock
        sql = "UPDATE inventory SET stock=? WHERE id=?"
        c.execute(sql, (new_stock, product_id[x]))
        conn.commit()

        # insert into the transaction
        sql2 = "INSERT INTO transactions (product_name, quantity, amount, date) VALUES (?, ?, ?, ?)"
        c.execute(
            sql2, (products_list[x], product_quantity[x], product_price[x], date))
        conn.commit()

        x += 1

    for a in labels_list:
        a.destroy()

    del(products_list[:])
    del(product_id[:])
    del(product_quantity[:])
    del(product_price[:])

    c_amount.configure(text="")
    total_l.configure(text="")
    change_e.delete(0, END)
    enteride.focus()
    tkinter.messagebox.showinfo("Success", "Bill has been generated")


# frame1
left = Frame(frame1, width=700, height=768, bg='floral white')
left.pack(side=LEFT)

right = Frame(frame1, width=666, height=768, bg='orange')
right.pack(side=RIGHT)

# components
heading = Label(left, text="General Store", font=(
    'arial 40 bold'), bg='floral white')
heading.place(x=0, y=0)

date_label = Label(right, text="Today's Date: " +
                   str(date), font=('arial 16 bold'), bg='orange', fg='white')
date_label.place(x=0, y=0)

# table invoice==============================================================
tproduct = Label(right, text="Products", font=(
    'arial 16 bold'), bg='orange', fg='white')
tproduct.place(x=0, y=60)

tquantity = Label(right, text="Quantity", font=(
    'arial 16 bold'), bg='orange', fg='white')
tquantity.place(x=280, y=60)

tamount = Label(right, text="Amount", font=(
    'arial 16 bold'), bg='orange', fg='white')
tamount.place(x=480, y=60)

# enter stuff
enterid = Label(left, text="Enter Product's ID", font=(
    'arial 18 bold'), bg='floral white')
enterid.place(x=0, y=80)

enteride = Entry(left, width=12, font=(
    'arial 18 bold'), bg='orange')
enteride.place(x=230, y=80)
enteride.focus()

# button
search_btn = Button(
    left, text="Search", font=('arial 10 bold'), width=15, height=1, bg='green', fg="white", activebackground='white', activeforeground='black', command=ajax)
search_btn.place(x=400, y=80)

# fill it later by the function ajax
productname = Label(left, text="", font=(
    'arial 27 bold'), bg='floral white', fg='steelblue')
productname.place(x=0, y=250)

pprice = Label(left, text="", font=(
    'arial 27 bold'), bg='floral white', fg='steelblue')
pprice.place(x=0, y=290)

# total label
total_l = Label(right, text="", font=(
    'arial 40 bold'), bg='orange', fg='white')
total_l.place(x=0, y=600)

frame1.bind("<Return>", ajax)
frame1.bind("<Up>", add_to_cart)
frame1.bind("<space>", generate_bill)

Prod_List = Label(frame1, text="Product list : ",
                  font=('arial 16 bold'), bg='floral white')
Prod_List.place(x=90, y=120)
# Combobox creation
n = StringVar()
ProductList = ttk.Combobox(frame1, width=18, textvariable=n)


c.execute("SELECT id, name from inventory")

tuples = c.fetchall()
product_tuple = [i for i in tuples]


products = ["Product List"]
for i, p in product_tuple:
    product = str(i) + "   " + str(p)

    products.append(product)


# Adding combobox drop down list
ProductList['values'] = products
ProductList.place(x=250, y=125)
ProductList.current(0)

# create the quantity and the discount label
quantity_l = Label(left, text="Enter Quantity", font=(
    'arial 18 bold'), bg='floral white')
quantity_l.place(x=0, y=370)

quantity_e = Entry(left, width=25,
                   font=('arial 18 bold'), bg='orange')
quantity_e.place(x=190, y=370)
quantity_e.focus()

# discount
discount_l = Label(left, text="Enter Discount", font=(
    'arial 18 bold'), bg='floral white')
discount_l.place(x=0, y=410)

discount_e = Entry(left, width=25,
                   font=('arial 18 bold'), bg='orange')
discount_e.place(x=190, y=410)
discount_e.insert(END, 0)

# add to cart button
add_to_cart_btn = Button(
    left, text="Add To Cart", width=22, height=2, bg='green', fg="white", activebackground='white', activeforeground='black', command=add_to_cart)
add_to_cart_btn.place(x=350, y=450)

# generate bill and change
change_l = Label(left, text="Given Amount", font=(
    'arial 18 bold'), bg='floral white')
change_l.place(x=0, y=550)

change_e = Entry(left, width=25, font=(
    'arial 18 bold'), bg='orange')
change_e.place(x=200, y=550)

# button change
change_btn = Button(left, text="Calculate Change",
                    width=22, height=2, bg='green', fg="white", activebackground='white', activeforeground='black', command=change_func)
change_btn.place(x=360, y=590)

# generate bill button
bill_btn = Button(left, text="Generate Bill", width=100,
                  height=2, bg='red', fg='white', command=generate_bill)
bill_btn.place(x=0, y=640)

c_amount = Label(left, text="",
                 font=('arial 18 bold'), fg='red', bg='floral white')

get_stock = 0
get_name = 0
get_id = 0
get_price = 0


update_btn = Button(left, text="Update",
                    height=2, bg='green', fg='white', command=lambda: show_frame(frame3))
update_btn.place(x=30, y=690)

add_btn = Button(left, text="Add products",
                 height=2, bg='green', fg='white', command=lambda: show_frame(frame2))
add_btn.place(x=150, y=690)

logout_btn1 = Button(left, text="Logout",
                     height=2, bg='green', fg='white', command=lambda: show_frame(frame4))
logout_btn1.place(x=300, y=690)


# --------------------------------------------Add to database----------------------------------------
# functions in frame 2

def isnumber(num_string):
    if re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9,10}$', num_string):
        return True
    return False


def get_items():
    # get from entries
    global cp2_e, sp2_e

    vendor_phone = vendor_phone_e.get()

    if isnumber(vendor_phone):
        name = name2_e.get()
        stock = stock2_e.get()
        cp = cp2_e.get()
        sp = sp2_e.get()
        vendor = vendor_e.get()
        # dynamic entries
        totalcp = int(cp) * int(stock)
        totalsp = int(sp) * int(stock)
        assumed_profit = int(totalsp - totalcp)

        if name == '' or stock == '' or cp == '' or sp == '':
            tkinter.messagebox.showinfo(
                "Error", "Please Fill all the entries.")
        else:
            sql = "INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno ) VALUES(?,?,?,?,?,?,?,?,?)"
            c.execute(sql, (name, stock, cp, sp, totalcp, totalsp,
                            assumed_profit, vendor, vendor_phone))
            conn.commit()

            result = c.execute("SELECT Max(id) from inventory")
            for r in result:
                id = r[0]

            tBox2.config(text="")
            tBox3.config(text="")

            # textbox insert

            tBox2.config(text="ID has reached upto: " + str(id)+"\n\nInserted " + str(name) +
                         " into the database with code " + str(id_e.get()), bg="white")
            tBox3.config(text="ID has reached upto: " + str(id), bg="white")

            tkinter.messagebox.showinfo(
                "Success", "Successfully added to the database")

            n = StringVar()
            ProductList = ttk.Combobox(frame1, width=18, textvariable=n)
            ProductList2 = ttk.Combobox(frame2, width=18, textvariable=n)
            ProductList3 = ttk.Combobox(frame3, width=18, textvariable=n)
            products = []
            c.execute("SELECT id, name from inventory")

            tuples = c.fetchall()
            product_tuple = [i for i in tuples]

            products = ["Product List"]
            for i, p in product_tuple:
                product = str(i) + "   " + str(p)
                products.append(product)
            # Adding combobox drop down list
            ProductList['values'] = products
            ProductList2['values'] = products
            ProductList3['values'] = products

            ProductList3.place(x=200, y=80)
            ProductList3.current(0)

            ProductList2.place(x=240, y=80)
            ProductList2.current(0)

            ProductList.place(x=250, y=125)
            ProductList.current(0)
    else:
        tkinter.messagebox.showinfo("Error", "Invalid phone number")


def clear_all():
    global name2_e, stock2_e, cp2_e, sp2_e, vendor_e, vendor_phone_e
    num = id + 1
    name2_e.delete(0, END)
    stock2_e.delete(0, END)
    cp2_e.delete(0, END)
    sp2_e.delete(0, END)
    vendor_e.delete(0, END)
    vendor_phone_e.delete(0, END)


result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]

heading = Label(frame2, text="Add to the database",
                font=('arial 40 bold'), fg='steelblue')
heading.place(x=400, y=0)

# labels  for the window
name_l = Label(frame2, text="Enter Product Name", font=('arial 18 bold'))
name_l.place(x=0, y=70)

stock_l = Label(frame2, text="Enter Stocks", font=('arial 18 bold'))
stock_l.place(x=0, y=120)

cp_l = Label(frame2, text="Enter Cost Price", font=('arial 18 bold'))
cp_l.place(x=0, y=170)

sp_l = Label(frame2, text="Enter Selling Price", font=('arial 18 bold'))
sp_l.place(x=0, y=220)

vendor_l = Label(frame2, text="Enter Vendor Name", font=('arial 18 bold'))
vendor_l.place(x=0, y=270)

vendor_phone_l = Label(
    frame2, text="Enter Vendor Phone Number", font=('arial 18 bold'))
vendor_phone_l.place(x=0, y=320)

id_l = Label(frame2, text="Enter Vendor ID", font=('arial 18 bold'))
id_l.place(x=0, y=370)
# entries for the labels
name2_e = Entry(frame2, width=25, font=('arial 18 bold'))
name2_e.place(x=380, y=70)

stock2_e = Entry(frame2, width=25, font=('arial 18 bold'))
stock2_e.place(x=380, y=120)

cp2_e = Entry(frame2, width=25, font=('arial 18 bold'))
cp2_e.place(x=380, y=170)

sp2_e = Entry(frame2, width=25, font=('arial 18 bold'))
sp2_e.place(x=380, y=220)

vendor_e = Entry(frame2, width=25, font=('arial 18 bold'))
vendor_e.place(x=380, y=270)

vendor_phone_e = Entry(frame2, width=25, font=('arial 18 bold'))
vendor_phone_e.place(x=380, y=320)

id_e = Entry(frame2, width=25, font=('arial 18 bold'))
id_e.place(x=380, y=370)

# button to add to the database
btn_add = Button(frame2, text="Add To Database", width=25,
                 height=2, bg='steelblue', fg='white', command=get_items)
btn_add.place(x=520, y=420)

btn_clear = Button(frame2, text="Clear All Fields", width=18,
                   height=2, bg='lightgreen', fg='white', command=clear_all)
btn_clear.place(x=350, y=420)

# text box for the logs
tBox2 = Label(frame2, width=60, height=18, font=('arial 12 bold'))
tBox2.place(x=750, y=70)
tBox2.config(text="ID has reached upto: " + str(id), bg="white")

frame2.bind('<Return>', get_items)
frame2.bind('<Up>', clear_all)

# Combobox creation
n = StringVar()
ProductList3 = ttk.Combobox(frame2, width=18, textvariable=n)

products = []
c.execute("SELECT id, name from inventory")

tuples = c.fetchall()
product_tuple = []
for i in tuples:
    product_tuple.append(i)

products = ["Product List"]
for i, p in product_tuple:
    product = str(i) + "   " + str(p)

    products.append(product)


# Adding combobox drop down list
ProductList3['values'] = products

ProductList3.place(x=240, y=80)
ProductList3.current(0)


home_btn = Button(frame2, text="Home",
                  height=2, bg='green', fg='white', command=lambda: show_frame(frame1))
home_btn.place(x=30, y=690)


update_btn = Button(frame2, text="Update products",
                    height=2, bg='green', fg='white', command=lambda: show_frame(frame3))
update_btn.place(x=150, y=690)

logout_btn2 = Button(frame2, text="Logout",
                     height=2, bg='green', fg='white', command=lambda: show_frame(frame4))
logout_btn2.place(x=300, y=690)

# --------------------------------------------Update database----------------------------------------

# frame 3 functions


def search():
    sql = "SELECT * FROM inventory WHERE id=?"
    result = c.execute(sql, (id_leb.get(), ))
    n1 = None  # name
    n2 = None  # stock
    n3 = None  # cp
    n4 = None  # sp
    n5 = None  # totalcp
    n6 = None  # totalsp
    n7 = None  # assumed_profit
    n8 = None  # vendor
    n9 = None  # vendor_phone
    for r in result:
        n1 = r[1]  # name
        n2 = r[2]  # stock
        n3 = r[3]  # cp
        n4 = r[4]  # sp
        n5 = r[5]  # totalcp
        n6 = r[6]  # totalsp
        n7 = r[7]  # assumed_profit
        n8 = r[8]  # vendor
        n9 = r[9]  # vendor_phone
    conn.commit()

    # insert into the entries to update
    name3_e.delete(0, END)
    name3_e.insert(0, str(n1))

    stock3_e.delete(0, END)
    stock3_e.insert(0, str(n2))

    cp3_e.delete(0, END)
    cp3_e.insert(0, str(n3))

    sp3_e.delete(0, END)
    sp3_e.insert(0, str(n4))

    vendor3_e.delete(0, END)
    vendor3_e.insert(0, str(n8))

    vendor_phone3_e.delete(0, END)
    vendor_phone3_e.insert(0, str(n9))

    totalcp_e.delete(0, END)
    totalcp_e.insert(0, str(n5))

    totalsp_e.delete(0, END)
    totalsp_e.insert(0, str(n6))


def update():

    u8 = vendor_phone3_e.get()

    if isnumber(u8):
        # get all the updated values
        u1 = name3_e.get()
        u2 = stock3_e.get()
        u3 = cp3_e.get()
        u4 = sp3_e.get()
        u5 = totalcp_e.get()
        Mysp = int(totalsp_e.get())
        # u6 = (int(totalcp_e.get()) / int(cp_e.get()) ) * int(sp_e.get())
        u6 = (Mysp / (int(totalcp_e.get()) / int(cp3_e.get()))) * ((int(totalcp_e.get()) /int(cp3_e.get())) - int(stock3_e.get())) + int(sp3_e.get()) * int(stock3_e.get())
        u7 = vendor3_e.get()
        query = "UPDATE inventory SET name=?, stock=?, cp=?, sp=?, totalcp=?, totalsp=?, vendor=?, vendor_phoneno=? WHERE id=?"
        c.execute(query, (u1, u2, u3, u4, u5, u6, u7, u8, id_leb.get()))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Update database Successful")

        n = StringVar()
        ProductList = ttk.Combobox(frame1, width=18, textvariable=n)
        ProductList2 = ttk.Combobox(frame2, width=18, textvariable=n)
        ProductList3 = ttk.Combobox(frame3, width=18, textvariable=n)
        products = []
        c.execute("SELECT id, name from inventory")

        tuples = c.fetchall()
        product_tuple = [i for i in tuples]

        products = ["Product List"]
        for i, p in product_tuple:
            product = str(i) + "   " + str(p)
            products.append(product)
        # Adding combobox drop down list
        ProductList['values'] = products
        ProductList2['values'] = products
        ProductList3['values'] = products

        ProductList3.place(x=200, y=80)
        ProductList3.current(0)

        ProductList2.place(x=240, y=80)
        ProductList2.current(0)

        ProductList.place(x=250, y=125)
        ProductList.current(0)
    else:
        tkinter.messagebox.showinfo("Error", "Invalid phone number")


result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]


heading = Label(frame3, text="Update the database",
                font=('arial 40 bold'), fg='steelblue')
heading.place(x=400, y=0)

# label and entry for id
id_le = Label(frame3, text="Enter Id", font=('arial 18 bold'))
id_le.place(x=0, y=70)

id_leb = Entry(frame3, font=('arial 18 bold'), width=10)
id_leb.place(x=380, y=70)

# Combobox creation
n = StringVar()
ProductList = ttk.Combobox(frame3, width=18, textvariable=n)

products = []
c.execute("SELECT id, name from inventory")

tuples = c.fetchall()
product_tuple = []
for i in tuples:
    product_tuple.append(i)

products = ["Product List"]
for i, p in product_tuple:
    product = str(i) + "   " + str(p)
    products.append(product)


# Adding combobox drop down list
ProductList['values'] = products

ProductList.place(x=200, y=80)
ProductList.current(0)

btn_search = Button(frame3, text="Search", width=15,
                    height=2, bg='orange', command=search)
btn_search.place(x=550, y=70)
# labels  for the window
name_l = Label(frame3, text="Enter Product Name", font=('arial 18 bold'))
name_l.place(x=0, y=120)

stock_l = Label(frame3, text="Enter Stocks", font=('arial 18 bold'))
stock_l.place(x=0, y=170)

cp_l = Label(frame3, text="Enter Cost Price", font=('arial 18 bold'))
cp_l.place(x=0, y=220)

sp_l = Label(frame3, text="Enter Selling Price", font=('arial 18 bold'))
sp_l.place(x=0, y=270)

totalcp_l = Label(frame3, text="Enter Total Cost Price",
                  font=('arial 18 bold'))
totalcp_l.place(x=0, y=320)

totalsp_l = Label(frame3, text="Enter Total Selling Price",
                  font=('arial 18 bold'))
totalsp_l.place(x=0, y=370)

vendor_l = Label(frame3, text="Enter Vendor Name", font=('arial 18 bold'))
vendor_l.place(x=0, y=420)

vendor_phone_l = Label(
    frame3, text="Enter Vendor Phone Number", font=('arial 18 bold'))
vendor_phone_l.place(x=0, y=470)

# entries for the labels
name3_e = Entry(frame3, width=25, font=('arial 18 bold'))
name3_e.place(x=380, y=120)

stock3_e = Entry(frame3, width=25, font=('arial 18 bold'))
stock3_e.place(x=380, y=170)

cp3_e = Entry(frame3, width=25, font=('arial 18 bold'))
cp3_e.place(x=380, y=220)

sp3_e = Entry(frame3, width=25, font=('arial 18 bold'))
sp3_e.place(x=380, y=270)

totalcp_e = Entry(frame3, width=25, font=('arial 18 bold'))
totalcp_e.place(x=380, y=320)

totalsp_e = Entry(frame3, width=25, font=('arial 18 bold'))
totalsp_e.place(x=380, y=370)

vendor3_e = Entry(frame3, width=25, font=('arial 18 bold'))
vendor3_e.place(x=380, y=420)

vendor_phone3_e = Entry(frame3, width=25, font=('arial 18 bold'))
vendor_phone3_e.place(x=380, y=470)

# button to add to the database
btn_add = Button(frame3, text="Update Database", width=25,
                 height=2, bg='steelblue', fg='white', command=update)
btn_add.place(x=520, y=520)

# text box for the logs
tBox3 = Label(frame3, width=60, height=18, font=('arial 12 bold'))
tBox3.place(x=750, y=70)
tBox3.config(text="ID has reached upto: " + str(id), bg="white")


home_btn = Button(frame3, text="Home",
                  height=2, bg='green', fg='white', command=lambda: show_frame(frame1))
home_btn.place(x=30, y=690)


add_btn = Button(frame3, text="Add products",
                 height=2, bg='green', fg='white', command=lambda: show_frame(frame2))
add_btn.place(x=150, y=690)

logout_btn3 = Button(frame3, text="Logout",
                     height=2, bg='green', fg='white', command=lambda: show_frame(frame4))
logout_btn3.place(x=300, y=690)

# --------------------------------------------Login----------------------------------------

# frame 4 functions

Username = "admin"
Password = "admin"


def auth_login(Uname, Passwd):
    if Uname == Username and Passwd == Password:
        show_frame(frame1)
        Uname_e.delete(0, END)
        Passwd_e.delete(0, END)
    else:
        tkinter.messagebox.showinfo(
            "Error", "Incorrect login Credentials")


canvas = Canvas(frame4, width=725, height=384)
canvas.place(x=335, y=140)

canvas.create_rectangle(0, 0, 725, 700, fill='orange', outline="white")

heading = Label(frame4, text="General Store",
                font=('arial 52 bold'), fg='white', bg="blue")
heading.place(x=550, y=50)

heading = Label(frame4, text="Login",
                font=('arial 40 bold'), fg='white', bg="orange")
heading.place(x=600, y=150)

Dashes = Label(frame4, text="--------------------------------------",
               font=('arial 40 bold'), fg='white', bg="orange")
Dashes.place(x=350, y=225)

Uname_l = Label(frame4, text="Username :", font=(
    'arial 18 bold'), fg='white', bg="orange")
Uname_l.place(x=500, y=350)

Uname_e = Entry(frame4, width=25, font=('arial 18 bold'))
Uname_e.place(x=683, y=350)


Passwd_l = Label(frame4, text="Password :", font=(
    'arial 18 bold'), fg='white', bg="orange")
Passwd_l.place(x=500, y=400)

Passwd_e = Entry(frame4, show='*', width=25, font=('arial 18 bold'))
Passwd_e.place(x=683, y=400)

Login_btn = Button(frame4, text="Login", font=(
    'arial 20'), width=7,
    height=1, bg='orange', fg='white', command=lambda: auth_login(Uname_e.get(), Passwd_e.get()))
Login_btn.place(x=660, y=450)


show_frame(frame4)
root.mainloop()
