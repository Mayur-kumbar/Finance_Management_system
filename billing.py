from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import sqlite3
import time
import os
import tempfile

# Give the path to save the bill as pdf file
new_file = "F:/Inventory_Management_System/BillsToPrint"


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1520x775+0+0")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.cart_list = []
        self.chk_print = 0

        # Title
        # image resizing
        self.title_icon = Image.open("image/inventory_10951884.png")
        self.title_icon = self.title_icon.resize((50, 50), Image.LANCZOS)
        self.title_icon = ImageTk.PhotoImage(self.title_icon)

        title = Label(self.root, text="Finance Management System", image=self.title_icon, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0,
                                                                                                                 y=0,
                                                                                                                 relwidth=1,
                                                                                                                 height=70)

        # logout button

        logout = Button(self.root,command=self.logout, text="Logout", font=("times new roman", 15, "bold"), bg="yellow",
                        cursor="hand2").place(x=1350, y=10, height=50, width=150)


        # sub title
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().time()
        self.clock = Label(self.root,
                           text=f"Welcome to Finance Management System\t\tDate: {current_date.strftime('%d-%m-%Y')}\t\tTime: {current_time.strftime('%H:%M')}",
                           font=("times new roman", 15), bg="#4d636d", fg="white")
        self.clock.place(x=0, y=70, relwidth=1, height=30)

        # =====ProductFrame=====
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        ProductFrame1.place(x=6, y=110, width=410, height=600)

        pTitle = Label(ProductFrame1, text='All Products', font=('goudy old style', 20, 'bold'), bg='#262626',
                       fg='white').pack(side=TOP, fill=X)

        # =====Search Product Frame=====
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg='white')
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text='Search Product | By Name ', font=('times new roman', 15, 'bold'),
                           bg='white', fg='green').place(x=2, y=5)

        lbl_name = Label(ProductFrame2, text='Product Name', font=('times new roman', 15, 'bold'), bg='white').place(
            x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=('times new roman', 15),
                           bg='lightyellow').place(x=130, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, bg='blue', font=('goudy old style', 15),
                            bd=1, relief=RIDGE, fg='white', cursor='hand2').place(x=285, y=47, width=100, height=23)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, cursor='hand2',
                              font=('goudy old style', 15), bd=1, relief=RIDGE, bg='red', fg='white').place(x=285, y=5,
                                                                                                            height=25,
                                                                                                            width=100)

        # Product detail using frame
        ProductFrame3 = Frame(ProductFrame1, bd=4, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=420)

        # scroll bars
        scrollY = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollX = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        # creating tree view class
        self.Product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "quantity", 'status'),
                                          yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        # packing scrollbars
        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)

        # setting scroll command property
        scrollX.config(command=self.Product_Table.xview)
        scrollY.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid", text="P ID")
        self.Product_Table.heading("name", text="Name")
        self.Product_Table.heading("price", text="Price")
        self.Product_Table.heading("quantity", text="QTY")
        self.Product_Table.heading("status", text="Status")

        self.Product_Table["show"] = "headings"

        # resizing the column width
        self.Product_Table.column('pid', width=40)
        self.Product_Table.column('name', width=100)
        self.Product_Table.column('price', width=100)
        self.Product_Table.column('quantity', width=40)
        self.Product_Table.column('status', width=90)

        self.Product_Table.pack(fill=BOTH, expand=1)

        self.Product_Table.bind('<ButtonRelease-1>', self.get_data)  # its a event  that calls get_data()

        lbl_note = Label(ProductFrame1, text="Note: 'Enter 0 QTY to Remove the Product from the Cart'", anchor='w',
                         font=('goudy old style', 12), bg='white', fg='black').pack(side=BOTTOM, fill=X)

        # =====CustomerFrame=====
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        CustomerFrame.place(x=455, y=110, width=600, height=100)

        cTitle = Label(CustomerFrame, text='Customer Details', font=('goudy old style', 20, 'bold'),
                       bg='lightgrey').pack(side=TOP, fill=X)

        lbl_CName = Label(CustomerFrame, text='Name', font=('times new roman', 15), bg='white').place(x=5, y=50)
        txt_CName = Entry(CustomerFrame, textvariable=self.var_cname, font=('times new roman', 15),
                          bg='lightyellow').place(x=55, y=50, width=170)

        lbl_Contact = Label(CustomerFrame, text='Contact No.', font=('times new roman', 15), bg='white').place(x=250,
                                                                                                               y=50,
                                                                                                               width=110)
        txt_Contact = Entry(CustomerFrame, textvariable=self.var_contact, font=('times new roman', 15),
                            bg='lightyellow').place(x=365, y=50, width=160)


        # =====Calculator & Cart Frame=====
        Calc_Cart_Frame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        Calc_Cart_Frame.place(x=455, y=210, width=600, height=390)

        # CalculatorFrame=====
        self.var_cal_input = StringVar()
        CalcFrame = Frame(Calc_Cart_Frame, bd=9, relief=RIDGE, bg='white')
        CalcFrame.place(x=5, y=10, width=285, height=365)
        
        txt_cal_input = Entry(CalcFrame, textvariable=self.var_cal_input, state='readonly', font=('arial', 15, 'bold'), justify=RIGHT, bd=10, relief=GROOVE, width=22).grid(row=0, columnspan=4)
        
        btn_7 = Button(CalcFrame, text='7', font=('Arial',15, 'bold'), command= lambda: self.get_input(7), bd=5, width=4, pady=13, cursor='hand2').grid(row=1, column=0)
        btn_8 = Button(CalcFrame, text='8', font=('Arial',15, 'bold'), command= lambda: self.get_input(8), bd=5, width=4, pady=13, cursor='hand2').grid(row=1, column=1)
        btn_9 = Button(CalcFrame, text='9', font=('Arial',15, 'bold'), command= lambda: self.get_input(9), bd=5, width=4, pady=13, cursor='hand2').grid(row=1, column=2)
        btn_sum = Button(CalcFrame, text='+', font=('Arial',15, 'bold'), command= lambda: self.get_input('+'), bd=5, width=4, pady=13, cursor='hand2').grid(row=1, column=3)
        
        btn_4 = Button(CalcFrame, text='4', font=('Arial',15, 'bold'), command= lambda: self.get_input(4), bd=5, width=4, pady=13, cursor='hand2').grid(row=2, column=0)
        btn_5 = Button(CalcFrame, text='5', font=('Arial',15, 'bold'), command= lambda: self.get_input(5), bd=5, width=4, pady=13, cursor='hand2').grid(row=2, column=1)
        btn_6 = Button(CalcFrame, text='6', font=('Arial',15, 'bold'), command= lambda: self.get_input(6), bd=5, width=4, pady=13, cursor='hand2').grid(row=2, column=2)
        btn_sub = Button(CalcFrame, text='-', font=('Arial',15, 'bold'), command= lambda: self.get_input('-'), bd=5, width=4, pady=13, cursor='hand2').grid(row=2, column=3)

        btn_1 = Button(CalcFrame, text='1', font=('Arial',15, 'bold'), command= lambda: self.get_input(1), bd=5, width=4, pady=13, cursor='hand2').grid(row=3, column=0)
        btn_2 = Button(CalcFrame, text='2', font=('Arial',15, 'bold'), command= lambda: self.get_input(2), bd=5, width=4, pady=13, cursor='hand2').grid(row=3, column=1)
        btn_3 = Button(CalcFrame, text='3', font=('Arial',15, 'bold'), command= lambda: self.get_input(3), bd=5, width=4, pady=13, cursor='hand2').grid(row=3, column=2)
        btn_mul = Button(CalcFrame, text='*', font=('Arial',15, 'bold'), command= lambda: self.get_input('*'), bd=5, width=4, pady=13, cursor='hand2').grid(row=3, column=3)
        
        btn_0 = Button(CalcFrame, text='0', font=('Arial',15, 'bold'), command= lambda: self.get_input(0), bd=5, width=4, pady=17, cursor='hand2').grid(row=4, column=0)
        btn_c = Button(CalcFrame, text='c', font=('Arial',15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=17, cursor='hand2').grid(row=4, column=1)
        btn_eq = Button(CalcFrame, text='=', font=('Arial',15, 'bold'), command=self.perform_cal, bd=5, width=4, pady=17, cursor='hand2').grid(row=4, column=2)
        btn_div = Button(CalcFrame, text='/', font=('Arial',15, 'bold'), command= lambda: self.get_input('/'), bd=5, width=4, pady=17, cursor='hand2').grid(row=4, column=3)
        
        # =====CartFrame=====
        CartFrame = Frame(Calc_Cart_Frame, bd=4, relief=RIDGE)
        CartFrame.place(x=290, y=10, width=300, height=365)
        self.cartTitle = Label(CartFrame, text="Cart \t Total Products: [ 0 ]", font=('goudy old style', 12),
                               bg='lightgrey')
        self.cartTitle.pack(side=TOP, fill=X)

        # scroll bars
        scrollY = Scrollbar(CartFrame, orient=VERTICAL)
        scrollX = Scrollbar(CartFrame, orient=HORIZONTAL)

        # creating tree view class
        self.Cart_Table = ttk.Treeview(CartFrame, columns=("pid", "name", "price", "quantity"),
                                       yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        # packing scrollbars
        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)

        # setting scroll command property
        scrollX.config(command=self.Cart_Table.xview)
        scrollY.config(command=self.Cart_Table.yview)

        self.Cart_Table.heading("pid", text="P ID")
        self.Cart_Table.heading("name", text="Name")
        self.Cart_Table.heading("price", text="Price")
        self.Cart_Table.heading("quantity", text="QTY")

        self.Cart_Table["show"] = "headings"

        # resizing the column width
        self.Cart_Table.column('pid', width=40)
        self.Cart_Table.column('name', width=90)
        self.Cart_Table.column('price', width=90)
        self.Cart_Table.column('quantity', width=30)

        self.Cart_Table.pack(fill=BOTH, expand=1)

        self.Cart_Table.bind('<ButtonRelease-1>', self.get_data_cart)  # its a event  that calls get_data()

        # =====Add Cart Widgets Frame=====
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgets_Frame = Frame(self.root, bd=2, relief=RIDGE)
        Add_CartWidgets_Frame.place(x=455, y=600, width=600, height=110)

        lbl_p_name = Label(Add_CartWidgets_Frame, text="Product Name", font=('times new roman', 15), bg='white').place(
            x=5, y=5)
        txt_p_name = Entry(Add_CartWidgets_Frame, textvariable=self.var_pname, font=('times new roman', 15),
                           bg='lightyellow', state='readonly').place(x=5, y=30, height=20, width=190)

        lbl_p_price = Label(Add_CartWidgets_Frame, text="Price per Qty", font=('times new roman', 15),
                            bg='white').place(x=235, y=5)
        txt_p_price = Entry(Add_CartWidgets_Frame, textvariable=self.var_price, font=('times new roman', 15),
                            bg='lightyellow', state='readonly').place(x=235, y=30, height=20, width=150)

        lbl_p_qty = Label(Add_CartWidgets_Frame, text="Quantity", font=('times new roman', 15), bg='white').place(x=420,
                                                                                                                  y=5)
        txt_p_qty = Entry(Add_CartWidgets_Frame, textvariable=self.var_qty, font=('times new roman', 15),
                          bg='lightyellow').place(x=420, y=30, height=20, width=125)

        self.lbl_inStock = Label(Add_CartWidgets_Frame, text="In Stock", font=('times new roman', 15), bg='white')
        self.lbl_inStock.place(x=5, y=60)

        btn_clear_cart = Button(Add_CartWidgets_Frame, text="Clear", command=self.clear_cart,
                                font=('times new roman', 15, 'bold'), bg='lightgrey', fg='white', bd=1, relief=RIDGE,
                                cursor='hand2').place(x=195, y=60, height=28, width=130)
        btn_add_cart = Button(Add_CartWidgets_Frame, text="Add | Update Cart", command=self.add_update_cart,
                              font=('times new roman', 15, 'bold'), bg='orange', fg='white', bd=1, relief=RIDGE,
                              cursor='hand2').place(x=365, y=60, height=28, width=180)

        # =====Billing Area=====
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=1100, y=110, width=410, height=470)

        bTitle = Label(billFrame, text='Customer Bill Area', font=('goudy old style', 20, 'bold'), bg='#262626',
                       fg='white').pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # =====Billing Buttons=====
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=1100, y=580, width=410, height=135)

        self.lbl_amt = Label(billMenuFrame, text='Bill Amount\n 0 ', font=('goudy old style', 15, 'bold'), bg='#3f51b5',
                             fg='white')
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text='Discount\n[5%]', font=('goudy old style', 15, 'bold'),
                                  bg='#8bc34a', fg='white')
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n 0 ', font=('goudy old style', 15, 'bold'), bg='#607d8b',
                                 fg='white')
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text='Print', command=self.print_bill, cursor='hand2',
                           font=('goudy old style', 15, 'bold'), bg='lightgreen', fg='white')
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, cursor='hand2',
                               font=('goudy old style', 15, 'bold'), bg='grey', fg='white')
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text='Generate\nSave Bill', command=self.generate_bill, cursor='hand2', font=('goudy old style', 15, 'bold'), bg='#009688', fg='white')

        btn_generate.place(x=246, y=80, width=160, height=50)

        # =====Footer=====
        footer = Label(self.root,
                       text="FMS- Finance Management System | Developed by FinTech Innovators\nFor any technical issue contact : 1234567890",
                       font=("times new roman", 12), bg="#4d636d", fg="white").pack(side="bottom", fill=X)

        self.show()

    # ===============================================All Functions=======================================

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            cur.execute("SELECT pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Enter proper inputs", parent=self.root)

            else:
                cur.execute(
                    "select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.Product_Table.delete(*self.Product_Table.get_children())
                    for row in rows:
                        self.Product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.Product_Table.focus()
        content = (self.Product_Table.item(f))
        row = content['values']

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.Cart_Table.focus()
        content = (self.Cart_Table.item(f))
        row = content['values']

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Quantity is Required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        else:
            # price_cal = float(int(self.var_qty.get()) * float(self.var_price.get()))
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

            # =====Update Cart=====
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1

            if present == 'yes':
                op = messagebox.askyesno('Confirm',
                                         "Product already present\nDo you want to Update | Remove from the Cart list?",
                                         parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2] = price_cal
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amt += (float(row[2]) * int(row[3]))

        self.discount = (self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount
        self.lbl_amt.config(text=f"Bill Amount\n{str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.Cart_Table.delete(*self.Cart_Table.get_children())
            for row in self.cart_list:
                self.Cart_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer Details are Required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add Product to the Cart", parent=self.root)

        else:
            # =====Bill Top=====
            self.bill_top()
            # =====Bill Middle=====
            self.bill_middle()
            # =====Bill Bottom=====
            self.bill_bottom()

            fp = open(f"bill/{str(self.invoice)}.txt", 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been Generated/Saved in Backend", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\tXYZ-Inventory
\t Phone No. 1234567890 , Belagavi-590006
{str('=' * 47)}
 Customer Name: {self.var_cname.get()}
 Ph No. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime('%d/%m/%Y'))}
{str('=' * 47)}
 Product Name:\t\t\tQTY\tPrice
{str('=' * 47)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = "Inactive"
                if int(row[3]) != int(row[4]):
                    status = "Active"
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n " + name + "\t\t\t" + row[3] + "\t\t\tRs." + price)
                # =====Update qty in Product Table=====
                cur.execute('Update product set qty=?,status=? where pid=?', (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str('=' * 47)}
 Bill Amount\t\t\t\tRs.{self.bill_amt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str('=' * 47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_search.set('')
        self.chk_print = 0
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.clear_cart()
        self.show()
        self.show_cart()

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            open(new_file, 'w').write(self.txt_bill_area.ge('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showinfo("Print", "Please Generate Bill, to print the receipt", parent=self.root)

    def logout(self):
       self.root.destroy()
       os.system("python login.py")

if __name__ == '__main__':
    root = Tk()

    obj = BillClass(root)
    root.mainloop()