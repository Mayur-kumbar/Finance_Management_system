from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import time

class employeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.root.focus_force()

        #======== All variables ========

        self.var_searchBy = StringVar()
        self.var_searchTxt = StringVar()

        self.var_ID=StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_address = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_pass = StringVar()
        self.var_contact = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        #================================

        # Create search frame
        searchFrame = LabelFrame(self.root, text="Search Employee", font=("times new roman", 12, "bold"), bd=3, relief=RIDGE)
        searchFrame.place(x=250, y=20, width=600, height=70)  # Place searchFrame using place method

        # Create search frame contents
        cmb_search = ttk.Combobox(searchFrame,textvariable=self.var_searchBy,values=("Select","Employee ID","Email","Name","Contact"),state='readonly',font=("goudy old style",10))  # Create Combobox inside searchFrame
        cmb_search.place(x=10, y=10, width=180)  # Place Combobox inside searchFrame
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_searchTxt,font=("goudy old style",10),bg="lightyellow").place(x=210,y=8,width = 180,height=25) #text box
        btn_search=Button(searchFrame,text="Search",command=self.search,font=("goudy old style",10,"bold"),bg='#4caf50',cursor="hand2").place(x=410,y=4,width=150,height=30)

        # main title
        title=Label(self.root,text="Employee Details",font=("times new roman",15,"bold"),bg='#0f4d7d',fg='white').place(x=50,y=100,width=1000)

        # main content

        # 1st row
        lbl_ID=Label(self.root,text="User ID",font=("goudy old style",12)).place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style", 12)).place(x=420, y=150)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style", 12)).place(x=770, y=150)


        unique_ID=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        self.var_ID.set(unique_ID%1000)
        txt_ID=Entry(self.root,textvariable=self.var_ID,font=("goudy old style",12),bg='lightyellow').place(x=150,y=150,width=180)

        txt_gender=ttk.Combobox(self.root, textvariable=self.var_gender,values=("Select", "Male", "Female", "Other"), state='readonly',font=("goudy old style", 10))  # Create Combobox
        txt_gender.place(x=500, y=150, width=180)  # Place Combobox
        txt_gender.current(0)

        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style", 12),bg='lightyellow').place(x=850, y=150,width=180)


        # 2nd row
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 12)).place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 12)).place(x=420, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 12)).place(x=770, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 12), bg='lightyellow').place(x=150,y=190,width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 12), bg='lightyellow').place(x=500,y=190,width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 12), bg='lightyellow').place(x=850,y=190,width=180)


        # 3rd row
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 12)).place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 12)).place(x=420, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 12)).place(x=770, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 12), bg='lightyellow').place(x=150,y=230,width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 12), bg='lightyellow').place(x=500,y=230,width=180)

        txt_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Select", "Admin", "Employee"),state='readonly', font=("goudy old style", 10))  # Create Combobox
        txt_utype.place(x=850, y=230, width=180)  # Place Combobox
        txt_utype.current(0)


        # 4th row
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 12)).place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 12)).place(x=500, y=270)

        self.var_address=Text(self.root,font=("goudy old style",12),bg='lightyellow')
        self.var_address.place(x=150,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",12),bg="lightyellow").place(x=555,y=270,width=180)


        # buttons in main contents

        btn_save=Button(self.root,text="Save",command=self.save,font=("goudy old style",12),bg="#2196f3",fg='white',cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update = Button(self.root, text="Update",command=self.update, font=("goudy old style", 12), bg="#4caf50", fg='white',cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("goudy old style", 12), bg="#f44336", fg='white',cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 12), bg="#607d8b", fg='white',cursor="hand2").place(x=860, y=305, width=110, height=28)


        # employee details using tree views

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)  #frame

        # scroll bars
        scrollY=Scrollbar(emp_frame,orient=VERTICAL)
        scrollX=Scrollbar(emp_frame,orient=HORIZONTAL)

        #creating tree view class
        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("ID","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrollY.set,xscrollcommand=scrollX.set)

        #packing scrollbars
        scrollX.pack(side=BOTTOM,fill=X)
        scrollY.pack(side=RIGHT,fill=Y)

        # setting scroll command property
        scrollX.config(command=self.EmployeeTable.xview)
        scrollY.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("ID",text="Employee ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"]="headings" # hiding default column

        #resizing the column width
        self.EmployeeTable.column("ID",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=100)
        self.EmployeeTable.column("salary",width=100)

        self.EmployeeTable.pack(fill=BOTH,expand=1)

        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data) # its a event to that calls get_data()

        self.show()
#--------------------------------------------- function for buttons -----------------------------------------------------

    def save(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
            if self.var_ID.get()=="":
                messagebox.showerror("Error","Employee ID Required",parent=self.root)
            else:
                cur.execute("SELECT * from employee where ID=?",(self.var_ID.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","ID Already Assigned\nTry Different",parent=self.root)
                else:
                    cur.execute("Insert into employee (ID,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_ID.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.var_address.get('1.0',END),
                        self.var_salary.get(),
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
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due ",parent=self.root)


    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']

        self.var_ID.set(row[0]),
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])

        self.var_address.delete('1.0', END)
        self.var_address.insert(END,row[9])

        self.var_salary.set(row[10])


    def update(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_ID.get() == "":
                messagebox.showerror("Error", "Employee ID Required", parent=self.root)
            else:
                cur.execute("SELECT * from employee where ID=?", (self.var_ID.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Employee ID Not Found", parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where ID=?",(

                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.var_address.get('1.0', END),
                            self.var_salary.get(),
                            self.var_ID.get(),
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
            if self.var_ID.get()=="":
                messagebox.showerror("Error","Employee ID Required",parent=self.root)
            else:
                cur.execute("Select * from employee where ID=?",(self.var_ID.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    check=messagebox.askyesno("Conform",f"Do you want to delete Employee ID: {self.var_ID.get()}")
                    if check==True:
                        cur.execute("delete from employee where ID=?",(self.var_ID.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Record Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def clear(self):
        unique_ID = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        self.var_ID.set(unique_ID%1000)
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("select")

        self.var_address.delete('1.0', END)

        self.var_salary.set("")

        self.var_searchBy.set("Select")
        self.var_searchTxt.set("")

        self.show()


    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        try:
            if self.var_searchBy.get()=='Select':
                messagebox.showerror("Error","Select Search Type",parent=self.root)
            elif self.var_searchTxt.get()=="":
                messagebox.showerror("Error","Enter proper inputs",parent=self.root)
            elif self.var_searchBy.get()=="Employee ID":
                cur.execute("SELECT * FROM employee WHERE ID=?",(self.var_searchTxt.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Employee ID Not Found",parent=self.root)
                else:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    self.EmployeeTable.insert('',END,values=row)

            else:
                cur.execute("select * from employee where "+self.var_searchBy.get()+" LIKE '%"+self.var_searchTxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error","No Record found",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
