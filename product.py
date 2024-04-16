from tkinter import *
#from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.root.focus_force()

        #----------------- All Variable ------------------
        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()

        self.cat_list=[]
        self.sup_list=[]
        self.get_cat_sup()
        
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        #--------------------------------------------------

        # Left frame
        left_frame=Frame(self.root,bd=3,relief=RIDGE)
        left_frame.place(x=10,y=10,width=480,height=480)

        # left frame title
        left_title=Label(left_frame,text="Manage Product Details",font=("times new roman",15,"bold"),bg='#0f4d7d',fg='white').pack(side=TOP,fill=X)

        # 1st row
        lbl_category=Label(left_frame,text="Category",font=("goudy old style",12)).place(x=50,y=40)
        cmb_category = ttk.Combobox(left_frame,textvariable=self.var_cat,values=self.cat_list, state='readonly',font=("goudy old style", 10))  # Create Combobox inside searchFrame
        cmb_category.place(x=140, y=42, width=180)  # Place Combobox inside searchFrame
        cmb_category.current(0)

        # 2nd row
        lbl_supplier = Label(left_frame, text="Supplier", font=("goudy old style", 12)).place(x=50, y=80)
        cmb_supplier = ttk.Combobox(left_frame,textvariable=self.var_sup, values=self.sup_list, state='readonly',font=("goudy old style", 10))  # Create Combobox inside searchFrame
        cmb_supplier.place(x=140, y=82, width=180)  # Place Combobox inside searchFrame
        cmb_supplier.current(0)

        # 3rd row
        lbl_name = Label(left_frame, text="Name", font=("goudy old style", 12)).place(x=50, y=120)
        txt_name=Entry(left_frame,textvariable=self.var_name,font=("goudy old style",12),bg="lightyellow").place(x=140,y=122,width=180)

        # 4th row
        lbl_price = Label(left_frame, text="Price", font=("goudy old style", 12)).place(x=50, y=160)
        txt_price = Entry(left_frame, textvariable=self.var_price, font=("goudy old style", 12), bg="lightyellow").place(x=140, y=162, width=180)

        # 5th row
        lbl_quantity = Label(left_frame, text="Quantity", font=("goudy old style", 12)).place(x=50, y=200)
        txt_quantity = Entry(left_frame, textvariable=self.var_qty, font=("goudy old style", 12),bg="lightyellow").place(x=140, y=202, width=180)

        # 6th row
        lbl_status = Label(left_frame, text="Status", font=("goudy old style", 12)).place(x=50, y=240)
        cmb_status = ttk.Combobox(left_frame, textvariable=self.var_status, values=("Select","Active","Inactive"), state='readonly',font=("goudy old style", 10))  # Create Combobox inside searchFrame
        cmb_status.place(x=140, y=242, width=180)  # Place Combobox inside searchFrame
        cmb_status.current(0)


        # Button
        btn_save=Button(left_frame,text="Save",command=self.save,font=("goudy old style",12),bg="#2196f3",fg='white',cursor="hand2").place(x=10,y=400,width=100,height=28)
        btn_update = Button(left_frame, text="Update",command=self.update, font=("goudy old style", 12), bg="#4caf50", fg='white',cursor="hand2").place(x=130, y=400, width=100, height=28)
        btn_delete = Button(left_frame, text="Delete",command=self.delete, font=("goudy old style", 12), bg="#f44336", fg='white',cursor="hand2").place(x=250, y=400, width=100, height=28)
        btn_clear = Button(left_frame, text="Clear",command=self.clear, font=("goudy old style", 12), bg="#607d8b", fg='white',cursor="hand2").place(x=370, y=400, width=100, height=28)

        # Create search frame
        searchFrame = LabelFrame(self.root, text="Search Employee", font=("times new roman", 12, "bold"), bd=3,relief=RIDGE)
        searchFrame.place(x=490, y=0, width=600, height=80)  # Place searchFrame using place method

        # Create search frame contents
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchBy,values=("Select","Category","Supplier","Name"), state='readonly',font=("goudy old style", 10))  # Create Combobox inside searchFrame
        cmb_search.place(x=10, y=10, width=180)  # Place Combobox inside searchFrame
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchTxt, font=("goudy old style", 10),bg="lightyellow").place(x=210, y=8, width=180, height=25)  # text box
        btn_search = Button(searchFrame, text="Search",command=self.search, font=("goudy old style", 10, "bold"),bg='#4caf50', cursor="hand2").place(x=410, y=4, width=150, height=30)


        # product detail using tree view
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=490, y=80,width=600, height=410)  # frame

        # scroll bars
        scrollY = Scrollbar(emp_frame, orient=VERTICAL)
        scrollX = Scrollbar(emp_frame, orient=HORIZONTAL)

        # creating tree view class
        self.ProductTable = ttk.Treeview(emp_frame, columns=("pid", "category", "supplier", "name", "price", "qty", "status"),yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        # packing scrollbars
        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)

        # setting scroll command property
        scrollX.config(command=self.ProductTable.xview)
        scrollY.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="Product ID")
        self.ProductTable.heading("category", text="Category")
        self.ProductTable.heading("supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Quantity")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"  # hiding default column

        # resizing the column width
        self.ProductTable.column("pid", width=90)
        self.ProductTable.column("category", width=100)
        self.ProductTable.column("supplier", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)

        self.ProductTable.pack(fill=BOTH, expand=1)

        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#--------------------------------------------------- Functions for Buttons ----------------------------------------------


    def get_cat_sup(self):
        con=sqlite3.connect(database="ims.db")
        cur=con.cursor()

        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup = cur.fetchall()
            self.sup_list.append("Empty")
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def save(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_cat.get() == "Select" or self.var_sup.get()=="Select" or self.var_name == "":
                messagebox.showerror("Error", "Category , Supplier , Name are must Required", parent=self.root)
            else:
                cur.execute("SELECT * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product Already Present\nTry Different", parent=self.root)
                else:
                    cur.execute("Insert into product (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Data Inserted Successfully", parent=self.root)
                    self.clear()


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            
            
    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            cur.execute("SELECT * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("select")

        self.var_searchBy.set("Select")
        self.var_searchTxt.set("")

        self.show()
    
    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']

        self.var_pid.set(row[0]),
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])


    def update(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select from the List", parent=self.root)
            else:
                cur.execute("SELECT * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Product Not Found", parent=self.root)
                else:
                    cur.execute("Update product set category=?,supplier=?,name=?,price=?,qty=?,status=? where pid=?",(

                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),

                            self.var_pid.get(),
                        ))
                    con.commit()
                    messagebox.showinfo("Success", "Record Updated Successfully", parent=self.root)
                    self.clear()

        except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            
            
    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select from the List",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Product Not Found",parent=self.root)
                else:
                    check=messagebox.askyesno("Conform",f"Do you want to delete Product ID: {self.var_pid.get()}")
                    if check==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Record Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
            
            
    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_searchBy.get()=='Select':
                messagebox.showerror("Error","Select Search Type",parent=self.root)
            elif self.var_searchTxt.get()=="":
                messagebox.showerror("Error","Enter proper inputs",parent=self.root)

            else:
                cur.execute("select * from product where "+self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error","No Record found",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)




if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
