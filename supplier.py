from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
import time

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.root.focus_force()

        #head title
        title=Label(self.root,text="Manage Supplier Details",font=("times new roman",20,"bold"),bg='#0f4d7d',fg='white')
        title.pack(side=TOP,fill=X)

        #------------- All Variable ----------------
        self.var_searchTxt=StringVar()

        self.var_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        #self.var_desc=StringVar()
        #--------------------------------------------

        # 1st row
        lbl_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",12)).place(x=25,y=50)
        unique_ID = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        self.var_invoice.set(unique_ID % 1000)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",12),bg="lightyellow").place(x=145,y=50,width=180)

        lbl_search=Label(self.root,text="Invoice No",font=("goudy old style",12)).place(x=650,y=50)
        txt_search=Entry(self.root,textvariable=self.var_searchTxt,font=("goudy old style",12),bg='lightyellow').place(x=730,y=50,width=180)

        # 2nd row
        lbl_name=Label(self.root,text="Supplier Name",font=("goudy old style",12)).place(x=25,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",12),bg="lightyellow").place(x=145,y=100,width=180)

        # 3rd row
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",12)).place(x=25,y=150)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",12),bg="lightyellow").place(x=145,y=150,width=180)

        # 4th row
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",12)).place(x=25,y=200)
        self.var_desc=Text(self.root,font=("goudy old style",12),bg="lightyellow")
        self.var_desc.place(x=145,y=200,width=350,height=100)

        # Buttons
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",12),bg='#2196f3',fg='white',cursor='hand2').place(x=915 ,y=45,width=133)

        btn_save = Button(self.root, text="Save",command=self.save, font=("goudy old style", 12), bg="#2196f3",fg='white', cursor="hand2").place(x=25, y=320, width=110, height=28)
        btn_update = Button(self.root, text="Update",command=self.update, font=("goudy old style", 12), bg="#4caf50",fg='white', cursor="hand2").place(x=145, y=320, width=110, height=28)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("goudy old style", 12), bg="#f44336",fg='white', cursor="hand2").place(x=265, y=320, width=110, height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 12), bg="#607d8b",fg='white', cursor="hand2").place(x=385, y=320, width=110, height=28)

        # supplier detail using frame
        supp_frame=Frame(self.root,bd=4,relief=RIDGE)
        supp_frame.place(x=650,y=80,width=400,height=400)

        # scroll bars
        scrollY = Scrollbar(supp_frame, orient=VERTICAL)
        scrollX = Scrollbar(supp_frame, orient=HORIZONTAL)

        # creating tree view class
        self.SupplierTable = ttk.Treeview(supp_frame, columns=("invoice", "name", "contact","desc"),yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        # packing scrollbars
        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)

        # setting scroll command property
        scrollX.config(command=self.SupplierTable.xview)
        scrollY.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice",text="Invoice No.")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("desc", text="Description")

        self.SupplierTable["show"]="headings"

        #resizing the column width
        self.SupplierTable.column('invoice',width=100)
        self.SupplierTable.column('name', width=100)
        self.SupplierTable.column('contact', width=100)
        self.SupplierTable.column('desc', width=100)

        self.SupplierTable.pack(fill=BOTH, expand=1)

        self.SupplierTable.bind('<ButtonRelease-1>',self.get_data)  # its a event  that calls get_data()

        self.show()

#--------------------------------------------- Function for Buttons ------------------------------------------------------

    def save(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Required")
            else:
                cur.execute("SELECT * from supplier where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()

                if row!=None:
                    messagebox.showerror("Error","Invoice No. Already Exist\nTry Different",parent=self.root)
                else:
                    cur.execute("INSERT into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                        self.var_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Data Inserted Successfully",parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            cur.execute("SELECT * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        unique_ID = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        self.var_invoice.set(unique_ID%1000)
        self.var_name.set("")
        self.var_contact.set("")
        self.var_desc.delete('1.0',END)

        self.var_searchTxt.set("")

        self.show()

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']

        self.var_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])

        self.var_desc.delete('1.0',END)
        self.var_desc.insert(END,row[3])


    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Required")
            else:
                cur.execute("SELECT * from supplier where invoice=? ",(self.var_invoice.get(),))
                row=cur.fetchone()

                if row == None:
                    messagebox.showerror("Error","Invoice No. Not Found")
                else:
                    cur.execute("UPDATE supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_desc.get('1.0',END),
                        self.var_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Record Updated Successfully")
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. Required")
            else:
                cur.execute("SELECT * from supplier where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invoice No. Not Found",parent=self.root)
                else:
                    check=messagebox.askyesno("Conform",f"Do you want to delete Invoice No.: {self.var_invoice.get()}")
                    if check==True:
                        cur.execute("DELETE from supplier where invoice = ?",(self.var_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Record Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_searchTxt.get()=="":
                messagebox.showerror("Error","Invoice No. Required")
            else:
                cur.execute("SELECT * from supplier where invoice=?",(self.var_searchTxt.get(),))
                row=cur.fetchone()

                if row==None:
                    messagebox.showerror("Error","Invoice No. Not Found")
                else:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

if __name__=="__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()