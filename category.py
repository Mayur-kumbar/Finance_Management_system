from tkinter import*
from tkinter import ttk,messagebox
import sqlite3

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.root.focus_force()

        #Title
        title=Label(self.root,text="Manage Product Category",font=("times new roman",20,"bold"),bg='#0f4d7d',fg='white').pack(side=TOP,fill=X,padx=20,pady=2)

        #--------- All Varialbe ---------------
        self.var_cid=StringVar()
        self.var_name=StringVar()
        #--------------------------------------

        # 1st row
        lbl_category=Label(self.root,text='Enter Category Name',font=("goudy old style",12)).place(x=40,y=70)
        txt_category=Entry(self.root,textvariable=self.var_name,font=("goudy old style",12),bg='lightyellow',bd=4,relief=RIDGE)
        txt_category.place(x=40,y=120,width=200,height=30)

        # Buttons
        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",12),bg='green',fg='white',cursor='hand2',bd=4,relief=RIDGE).place(x=260,y=117,width=125)
        btn_delete=Button(self.root,text="DELETE",command=self.delete,font=("goudy old style",12),bg='red',fg='white',cursor='hand2',bd=4,relief=RIDGE).place(x=400,y=117,width=125)

        # category Frame
        cat_frame = Frame(self.root, bd=4, relief=RIDGE)
        cat_frame.place(x=650, y=80, width=400, height=400)

        # scroll bars
        scrollY = Scrollbar(cat_frame, orient=VERTICAL)
        scrollX = Scrollbar(cat_frame, orient=HORIZONTAL)
        
        #creating tree view class
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

        # packing scrollbars
        scrollX.pack(side=BOTTOM, fill=X)
        scrollY.pack(side=RIGHT, fill=Y)

        # setting scroll command property
        scrollX.config(command=self.CategoryTable.xview)
        scrollY.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid",text="Category ID")
        self.CategoryTable.heading("name",text="Name")

        self.CategoryTable['show']="headings"

        self.CategoryTable.pack(fill=BOTH,expand=1)

        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data) # its a event  that calls get_data()

        self.show()
#--------------------------------------------------- function for buttons ----------------------------------------------

    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name is Required",parent=self.root)
            else:
                cur.execute("SELECT * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()

                if row!=None:
                    messagebox.showerror("Error","Category / Product already Exists",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Data inserted Successfully",parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            cur.execute("SELECT * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_cid.set("")
        self.var_name.set("")

        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']

        self.var_cid.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Select Product from List",parent=self.root)
            else:
                cur.execute("SELECT * from category where cid=?",(self.var_cid.get(),))
                row=cur.fetchone()

                if row == None:
                    messagebox.showerror("Error","Product not Found",parent=self.root)
                else:
                    check=messagebox.askyesno("Conform",f"Do you want to delete product: {self.var_name.get()}")
                    if check:
                        cur.execute("DELETE from category where cid=?",(self.var_cid.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Record Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


if __name__=="__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()