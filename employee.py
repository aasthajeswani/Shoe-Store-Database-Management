#==================imports===================
import sqlite3
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
import mariadb
import sys
from PIL import Image, ImageTk
# import mysql.connector
import re
#============================================



root = Tk()

root.geometry("1366x768")
root.title("Retail Manager")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()


Name = StringVar()
PhoneNumber = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()


# with sqlite3.connect("./Database/store.db") as db:
#     cur = db.cursor()
try:
    conn = mariadb.connect(
    user="root",
    password="aastha@123",
    host="127.0.0.1",
    port=3306,  # Default MariaDB port
    database="shoestoremanagement"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Create a cursor object using cursor() method
cur = conn.cursor()
    
# def random_bill_number(stringLength):
#     lettersAndDigits = string.ascii_letters.upper() + string.digits
#     strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
#     return ('BB'+strr)
generated_bill_numbers = set()

def random_bill_number():
    global generated_bill_numbers
    while True:
        bill_number = random.randint(6000, 9999)
        if bill_number not in generated_bill_numbers:
            generated_bill_numbers.add(bill_number)
            return bill_number

def valid_phone(phn):
    if re.match(r"[789]\d{9}$", phn):
        return True
    return False




def login(Event=None):
    global ManagerName
    ManagerName = user.get()
    ShopNo = passwd.get()

    
    try:
        conn = mariadb.connect(
        user="root",
        password="aastha@123",
        host="127.0.0.1",
        port=3306,  # Default MariaDB port
        database="shoestoremanagement"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Create a cursor object using cursor() method
    cur = conn.cursor()
    
    find_user = "SELECT * FROM store "
    cur.execute(find_user, [ManagerName, ShopNo])
    results = cur.fetchall()
    if results:
        messagebox.showinfo("Login Page", "The login is successful")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)
        root.withdraw()
        global biller
        global page2
        biller = Toplevel()
        page2 = bill_window(biller)
        page2.time()
        biller.protocol("WM_DELETE_WINDOW", exitt)
        biller.mainloop()

    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        page1.entry2.delete(0, END)



def logout():
    sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee_login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=login)


class Item:
    # def __init__(self, name, price, qty):
    #     self.Category = name
        
    #     self.Amount = price
    #     self.Qty = qty
    def __init__(self, prod, mrp, qty):
        self.prod=prod
        self.mrp = mrp
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.mrp * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.prod in self.dictionary):
                self.dictionary[i.prod] += i.qty
            else:
                self.dictionary.update({i.prod:i.qty})
    

def exitt():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()


class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Billing System")

        self.label = Label(biller)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        # image = Image.open("./images/bill_window1.png")
        # self.img = ImageTk.PhotoImage(image)
        self.img = PhotoImage(file="./images/bill_window3.png")
        self.label.configure(image=self.img)

        self.message = Label(biller)
        self.message.place(relx=0.038, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text=ManagerName)
        self.message.configure(anchor="w")

        self.clock = Label(biller)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(biller)
        self.entry1.place(relx=0.509, rely=0.23, width=240, height=24)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=Name)

        self.entry2 = Entry(biller)
        self.entry2.place(relx=0.791, rely=0.23, width=240, height=24)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(textvariable=PhoneNumber)

        self.entry3 = Entry(biller)
        self.entry3.place(relx=0.102, rely=0.22, width=240, height=24)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(textvariable=cust_search_bill)

        self.button1 = Button(biller)
        self.button1.place(relx=0.031, rely=0.104, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Logout""")
        self.button1.configure(command=logout)

        self.button2 = Button(biller)
        self.button2.place(relx=0.315, rely=0.234, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Search""")
        self.button2.configure(command=self.search_bill)

        self.button3 = Button(biller)
        self.button3.place(relx=0.048, rely=0.885, width=86, height=25)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 10")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""Total""")
        self.button3.configure(command=self.total_bill)

        self.button4 = Button(biller)
        self.button4.place(relx=0.141, rely=0.885, width=84, height=25)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 10")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""Generate""")
        self.button4.configure(command=self.gen_bill)

        self.button5 = Button(biller)
        self.button5.place(relx=0.230, rely=0.885, width=86, height=25)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 10")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""Clear""")
        self.button5.configure(command=self.clear_bill)

        self.button6 = Button(biller)
        self.button6.place(relx=0.322, rely=0.885, width=86, height=25)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 10")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""Exit""")
        self.button6.configure(command=exitt)

        self.button7 = Button(biller)
        self.button7.place(relx=0.098, rely=0.734, width=86, height=26)
        self.button7.configure(relief="flat")
        self.button7.configure(overrelief="flat")
        self.button7.configure(activebackground="#CF1E14")
        self.button7.configure(cursor="hand2")
        self.button7.configure(foreground="#ffffff")
        self.button7.configure(background="#CF1E14")
        self.button7.configure(font="-family {Poppins SemiBold} -size 10")
        self.button7.configure(borderwidth="0")
        self.button7.configure(text="""Add To Cart""")
        self.button7.configure(command=self.add_to_cart)

        self.button8 = Button(biller)
        self.button8.place(relx=0.274, rely=0.734, width=84, height=26)
        self.button8.configure(relief="flat")
        self.button8.configure(overrelief="flat")
        self.button8.configure(activebackground="#CF1E14")
        self.button8.configure(cursor="hand2")
        self.button8.configure(foreground="#ffffff")
        self.button8.configure(background="#CF1E14")
        self.button8.configure(font="-family {Poppins SemiBold} -size 10")
        self.button8.configure(borderwidth="0")
        self.button8.configure(text="""Clear""")
        self.button8.configure(command=self.clear_selection)

        self.button9 = Button(biller)
        self.button9.place(relx=0.194, rely=0.734, width=68, height=26)
        self.button9.configure(relief="flat")
        self.button9.configure(overrelief="flat")
        self.button9.configure(activebackground="#CF1E14")
        self.button9.configure(cursor="hand2")
        self.button9.configure(foreground="#ffffff")
        self.button9.configure(background="#CF1E14")
        self.button9.configure(font="-family {Poppins SemiBold} -size 10")
        self.button9.configure(borderwidth="0")
        self.button9.configure(text="""Remove""")
        self.button9.configure(command=self.remove_product)

        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(biller)
        self.combo1.place(relx=0.035, rely=0.359, width=477, height=26)

        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        find_gender = "SELECT distinct(Gender) FROM shoe"
        cur.execute(find_gender)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])

        self.combo1.configure(values=cat)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")


        self.combo2 = ttk.Combobox(biller)
        self.combo2.place(relx=0.035, rely=0.439, width=477, height=26)
        self.combo2.configure(font="-family {Poppins} -size 8")
        self.combo2.option_add("*TCombobox*Listbox.font", text_font) 
        self.combo2.configure(state="disabled")


        self.combo3 = ttk.Combobox(biller)
        self.combo3.place(relx=0.035, rely=0.510, width=477, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)
        
        
        self.combo4 = ttk.Combobox(biller)
        self.combo4.place(relx=0.035, rely=0.599, width=477, height=26)
        self.combo4.configure(state="disabled")
        self.combo4.configure(font="-family {Poppins} -size 8")
        self.combo4.option_add("*TCombobox*Listbox.font", text_font)


        self.entry4 = ttk.Entry(biller)
        self.entry4.place(relx=0.035, rely=0.679, width=477, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8")
        self.entry4.configure(foreground="#000000")
        self.entry4.configure(state="disabled")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)
        
    def get_category(self, Event):
        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        self.combo4.set('')
        find_category = "SELECT distinct(Category) FROM shoe where Gender =?"
        cur.execute(find_category, [self.combo1.get()])
        result2 = cur.fetchall()
        category = []
        for j in range(len(result2)):
            if(result2[j][0] not in category):
                category.append(result2[j][0])
        
        self.combo2.configure(values=category)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="readonly")

    def get_subcat(self, Event):
        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT distinct(Colour) FROM shoe WHERE Gender=?"
        cur.execute(find_product, [self.combo1.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])

        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.get_sizes)
        self.entry4.configure(state="disabled")
        
    def get_sizes(self, event):
        try:
            conn = mariadb.connect(
                user="root",
                password="aastha@123",
                host="127.0.0.1",
                port=3306,  # Default MariaDB port
                database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        
        self.combo4.configure(state="readonly")
        self.combo4.set('')
        
        find_sizes = "SELECT DISTINCT(Size) FROM shoe WHERE Gender = ?"
        cur.execute(find_sizes, [self.combo1.get()])
        sizes_result = cur.fetchall()
        
        sizes = []
        for k in range(len(sizes_result)):
            sizes.append(sizes_result[k][0])

        self.combo4.configure(values=sizes)
        # Bind a function to handle the selection event of combo4, if needed
        self.combo4.bind("<<ComboboxSelected>>", self.show_qty)
        # You can uncomment the line above and replace "self.some_function" with the function you want to call when a size is selected
        self.combo4.configure(state="readonly")
    
    def show_qty(self, Event):
        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        self.entry4.configure(state="normal")
        self.qty_label = Label(biller)
        self.qty_label.place(relx=0.033, rely=0.724, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        Gender=self.combo1.get()
        Category=self.combo2.get()
        Colour = self.combo3.get()
        Size=self.combo4.get()
        find_qty = "SELECT StockQuantity FROM shoe WHERE Gender=? and Category=? and Colour = ? and Size=?"
        cur.execute(find_qty, [Gender,Category,Colour,Size])
        results = cur.fetchone()
        if results is not None:  # Check if result is not None
            qty_in_stock = results[0]  # Extract the quantity from the result
            self.qty_label.configure(text="In Stock: {}".format(qty_in_stock))
        else:
            # Handle the case when no result is found
            self.qty_label.configure(text="In Stock: 0")
    
        # self.qty_label.configure(text="In Stock: {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")
        
    cart = Cart()
    def add_to_cart(self):
        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total')==-1:
            Gender=self.combo1.get()
            Category=self.combo2.get()
            Colour = self.combo3.get()
            Size = self.combo4.get()
            if(Category!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT Price, StockQuantity FROM shoe WHERE Gender=? and Category = ? and Colour =? and Size=?"
                cur.execute(find_mrp, [Gender,Category,Colour,Size])
                results = cur.fetchall()
                stock = int(results[0][1])
                mrp = int(results[0][0])
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = mrp*int(product_qty)
                        prod=Gender+" "+Category+" "+Colour+" "+Size
                        item = Item(prod, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(prod, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)
        else:
            self.Scrolledtext1.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i])!=0:
                    if li[i].find('Total')==-1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li)-1):
                self.Scrolledtext1.insert('insert', new_li[j])
                self.Scrolledtext1.insert('insert','\n')
            # Category = self.combo3.get()
            Gender=self.combo1.get()
            Category=self.combo2.get()
            Colour = self.combo3.get()
            Size=self.combo4.get()
            if(Category!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT Price, StockQuantity, ShoeId FROM shoe WHERE Gender =?,Category = ?,Colour=? and Size=?"
                cur.execute(find_mrp, [Gender,Category,Colour,Size])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = results[0][0]*int(product_qty)
                        prod=Gender+" "+Category+" "+Colour+" "+Size
                        item = Item(prod, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(prod, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert','\n')
                    
                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("Oops!", "Add a product.", parent=biller)

    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.514, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.894, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")
    
    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Oops!", "Add a product.", parent=biller)
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                self.Scrolledtext1.configure(state="normal")
                divider = "\n\n\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider)
                total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tRs. {}".format(self.cart.total())
                self.Scrolledtext1.insert('insert', total)
                divider2 = "\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider2)
                self.Scrolledtext1.configure(state="disabled")
            else:
                return

    state = 1
    def gen_bill(self):

        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if(Name.get()==""):
                messagebox.showerror("Oops!", "Please enter a name.", parent=biller)
            elif(PhoneNumber.get()==""):
                messagebox.showerror("Oops!", "Please enter a number.", parent=biller)
            elif valid_phone(PhoneNumber.get())==False: 
                messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("Oops!", "Cart is empty.", parent=biller)
            else: 
                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, Name.get())
                    self.name_message.configure(state="disabled")
            
                    self.num_message.insert(END, PhoneNumber.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number())

                    self.bill_message.insert(END, cust_new_bill.get())
                    self.bill_message.configure(state="disabled")
                    
                    bill_date.set(str(date.today().strftime("%d-%m-%Y")))

                    self.bill_date_message.insert(END, bill_date.get())
                    self.bill_date_message.configure(state="disabled")

                    try:
                        conn = mariadb.connect(
                        user="root",
                        password="aastha@123",
                        host="127.0.0.1",
                        port=3306,  # Default MariaDB port
                        database="shoestoremanagement"
                        )
                    except mariadb.Error as e:
                        print(f"Error connecting to MariaDB Platform: {e}")
                        sys.exit(1)

                    # Create a cursor object using cursor() method
                    cur = conn.cursor()
                    insert1 = (
                        "INSERT INTO customer(BillNo, Dates, Name, PhoneNumber, BillDetails) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert1, [cust_new_bill.get(), bill_date.get(), Name.get(), PhoneNumber.get(), self.Scrolledtext1.get('1.0', END)])
                    
                    select_shoe_query = "SELECT ShoeId FROM shoe WHERE Gender = ? AND Category = ? AND Colour = ? and Size =?"

                    # Execute the query with the selected shoe's attributes
                    cur.execute(select_shoe_query, [self.combo1.get(), self.combo2.get(), self.combo3.get(),self.combo4.get()])

                    # Fetch the ShoeId
                    shoe_id = cur.fetchone()[0]
                    
                    cur.execute("SELECT Price FROM shoe WHERE ShoeId = ?", [shoe_id])

                    # Fetch the result of the query
                    result = cur.fetchone()

                    
                    mrp = result[0]
                    
                    insert2=("INSERT INTO salestransaction(BillNo,Dates,ShoeId,Gender,Category,Colour,Qty,Amount) VALUES (?,?,?,?,?,?,?,?)")
                    cur.execute(insert2, [cust_new_bill.get(), bill_date.get(), shoe_id, self.combo1.get(), self.combo2.get(), self.combo3.get(), self.entry4.get(), mrp])

                    conn.commit()
                    # print(self.cart.items)
                    print(self.cart.allCart())
                    for prod, qty in self.cart.dictionary.items():
                        update_qty = "UPDATE shoe SET StockQuantity = StockQuantity - ? WHERE Gender=? and Category = ? and Colour=? and Size=?"
                        cur.execute(update_qty, [qty,self.combo1.get(), self.combo2.get(), self.combo3.get(), self.combo4.get() ])
                        conn.commit()
                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return
                    
    def clear_bill(self):
        self.wel_bill()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo4.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo4.delete(0,END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.combo4.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass
             
    def search_bill(self):
        try:
            conn = mariadb.connect(
            user="root",
            password="aastha@123",
            host="127.0.0.1",
            port=3306,  # Default MariaDB port
            database="shoestoremanagement"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Create a cursor object using cursor() method
        cur = conn.cursor()
        find_bill = "SELECT * FROM customer WHERE BillNo = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][0])
            self.name_message.configure(state="disabled")
    
            self.num_message.insert(END, results[0][1])
            self.num_message.configure(state="disabled")
    
            self.bill_message.insert(END, results[0][3])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][2])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.entry3.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

conn.close()
page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()

