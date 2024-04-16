from tkinter import *
from tkinter import ttk, messagebox
import os
import time
from PIL import Image,ImageTk
import datetime
from tkinter import ttk,messagebox
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import IMS

class dashBoard:
    def __init__(self, root):

        self.root = root
        self.root.geometry("1520x775+0+0")
        self.root.title("Finance Management System | Developed by FinTech Innovators")
        self.root.focus_force()

        # Title
        # image resizing
        self.title_icon = Image.open("image/inventory_10951884.png")
        self.title_icon = self.title_icon.resize((50, 50), Image.LANCZOS)
        self.title_icon = ImageTk.PhotoImage(self.title_icon)

        title = Label(self.root, text="Finance Management System", image=self.title_icon, compound=LEFT,font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0,y=0,relwidth=1,height=70)

        # logout button
        logout = Button(self.root,command=self.logout, text="Logout", font=("times new roman", 15, "bold"), bg="yellow",cursor="hand2").place(x=1350, y=10, height=50, width=150)

        # sub title
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().time()
        self.clock = Label(self.root, text="", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.clock.place(x=0, y=70, relwidth=1, height=30)

        self.update_clock()  # Update the clock initially

        self.graph_frame = Frame(self.root, bg="grey")
        self.graph_frame.place(x=730,y=100, height=625,width=800)

        # graph values
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        cur.execute("SELECT * FROM product")
        products = cur.fetchall()

        # Extract product names and values
        self.productName = [product[3] for product in products]  # Assuming product name is in the 4th column
        self.productvalue = [int(product[4]) * int(product[5]) for product in products]  # Assuming price and quantity are in 5th and 6th columns

        self.update_graph()

        # Labels
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", bg="#33bbf9", fg="white",font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_employee.place(x=25, y=270, height=150, width=300)

        # Total Supplier
        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", bg="#ff5722", fg="white",font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_supplier.place(x=360, y=270, height=150, width=300)

        # Total Product
        self.lbl_product = Label(self.root, text="Total Product\n[ 0 ]", bg="#607d8b", fg="white",font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_product.place(x=25, y=475, height=150, width=300)

        # Total Sales
        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bg="#ffc107", fg="white",font=("goudy old style", 20, "bold"), bd=5, relief=RIDGE)
        self.lbl_sales.place(x=360, y=475, height=150, width=300)

        # menu Button
        btn_menu=Button(self.root,text="Menu",command=self.main,font=('times new roman',15,'bold'),bg='orange',fg='white',cursor='hand2').place(x=25,y=170,width=180)

        self.update_lbl()

        # footer
        footer = Label(self.root,text="FMS- Finance Management System | Developed by FinTech Innovators\nFor any technical issue contact : 1234567890",font=("times new roman", 12), bg="#4d636d", fg="white").pack(side="bottom", fill=X)
#---------------------------------------------- Functions -----------------------------------------------

    def update_graph(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()

        # Fetch product data
        cur.execute("SELECT * FROM product")
        products = cur.fetchall()

        # Extract product names and values
        product_names = [product[3] for product in products]
        product_values = [int(product[4]) * int(product[5]) for product in products]

        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Create new figure
        figure = Figure(figsize=(8, 6), dpi=80)
        ax = figure.add_subplot(111)
        ax.bar(product_names, product_values, color='#11EA05')
        ax.set_xlabel("Product Name", fontsize=10)
        ax.set_ylabel("Product Sales", fontsize=10)
        ax.set_title("Product Stock Levels", fontsize=12)
        ax.tick_params(axis='x', labelrotation=90)

        # Draw canvas
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Schedule next update
        #self.root.after(5000, self.update_graph)

    #------------------------------------------------- Functions ---------------------------------------------

    def update_clock(self):
        # Get the current date and time
        current_date = datetime.date.today()

        # Format date and time as strings
        date_string = current_date.strftime("%Y-%m-%d")
        time_string = time.strftime('%H:%M')

        # Update the label text with formatted date and time
        self.clock.config(text=f"Welcome to Inventory Management System\t\tDate: {date_string}\t\tTime: {time_string}")

        # Schedule the update to run every second (1000 milliseconds)
        self.root.after(1000, self.update_clock)


    def update_lbl(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()

        try:
           cur.execute("select * from employee")
           employee=cur.fetchall()
           self.lbl_employee.config(text=f"Total Employee\n[{str(len(employee))}]")

           cur.execute("select * from product")
           product = cur.fetchall()
           self.lbl_product.config(text=f"Total Product\n[{str(len(product))}]")

           cur.execute("select * from supplier")
           supplier = cur.fetchall()
           self.lbl_supplier.config(text=f"Total Supplier\n[{str(len(supplier))}]")

           bill=len(os.listdir('bill'))
           self.lbl_sales.config(text=f"Total sales\n[{str(bill)}]")

           #time_=time.strftime("%I:%M:%S")
           #date_=time.strftime("%d-%m-%Y")

           self.clock.after(200,self.update_lbl)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def main(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = IMS(self.new_win)

    def logout(self):
       self.root.destroy()
       os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = dashBoard(root)
    root.mainloop()
