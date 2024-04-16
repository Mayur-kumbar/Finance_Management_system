from tkinter import*
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | Developed by FinTech Innovators")
        self.root.geometry("1520x775+0+0")

        self.otp=''


        #frame 1
        self.employee_id=StringVar()
        self.password=StringVar()
        
        login_frame=Frame(self.root ,bd=2 ,relief=RIDGE,bg="white")
        login_frame.place(x=550, y=90 ,width=350,height=500)
        title=Label(login_frame ,text="Login System", font=("Elephant",25,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Username",font=("Andalus",14),bg="white",fg="#767171").place(x=50,y=100)
       
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("Times new roman",14),bg="#ECECEC").place(x=50,y=140,width=240)
        
        lbl_password=Label(login_frame,text="Password",font=("Andalus",14),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(login_frame,textvariable=self.password,show="*",font=("Times new roman",14),bg="#ECECEC").place(x=50,y=240,width=240)

        btn=Button(login_frame, command=self.login, text="Log In",font=("Arial",14),bg="#00b0f0",fg="white",activebackground="#00b0f0",activeforeground="white",cursor="hand2").place(x=50,y=300,width=240,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=240,height=2)
        OR=Label(login_frame,text="OR",bg="white",font=("times new roman",14),fg="lightgray").place(x=150,y=358)

        btn_forgot=Button(login_frame,text="Forgot Password?",command=self.forget_window,font=("times new roman",14),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2").place(x=100,y=400)



    def login(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("error","All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where ID=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                     messagebox.showerror("error","invalid username or password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("error","employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where ID=? ",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                     messagebox.showerror("error","invalid employee ID, try again",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send email function
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("error","invalid employee ID ,try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('FORGET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text='Reset Password',font=("Times new roman",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on registered email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="blue",fg="white")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_conf_pass=Label(self.forget_win,text="Confirm password",font=("times new roman",15)).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="blue",fg="white")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_conf_pass.get():
             messagebox.showerror("error","New Password and confirm password should be same",parent=self.forget_win)
        else:
             con=sqlite3.connect(database='ims.db')
             cur=con.cursor()
             try:
                 cur.execute("Update employee SET pass=? where ID=?",(self.var_new_pass.get(),self.employee_id.get()))
                 con.commit()
                 messagebox.showinfo("success","Password updated succesfully")

             except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("error","invalid OTP ,try again",parent=self.forget_win)




    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        
        subj='FMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nFMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'



root=Tk()
obj=Login_System(root)
root.mainloop()
        