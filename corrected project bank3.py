from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import time
import sqlite3
import re
import random


try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_password text,acn_email text,acn_adhar text,acn_address text,acn_mob int,acn_bal float,acn_opendate text,acn_gender text,acn_type text)")
    conobj.close()
    print("Table created")
except:
    print("something went wrong,might be table already exists")

win=Tk()
win.state('zoomed')
win.configure(bg='pink')
win.resizable(width=False,height=False)

title=Label(win,text="Banking Automation",font=('arial',50,'bold','underline'),bg='pink')
title.pack()
title1=Label(win,text="By: ANJALI AGARWAL",font=('arial',15,'bold','underline'),bg='pink')
title1.place(relx=0,rely=.1)

dt=time.strftime("%d %B %Y,%A")
date=Label(win,text=f"{dt}",font=('arial',15,'bold'),bg='pink',fg='blue')
date.place(relx=.8,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def forgotpassword():
        frm.destroy()
        forgotpassword_screen()

    def newuser():
        frm.destroy()
        newuser_screen()

    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_password.get()
        
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("Validation","Empty fields are not allowed")
            return
        else:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from acn where acn_no=? and acn_password=?",(gacn,pwd))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Login","Invalid ACN/PASSWORD")
            else:
                frm.destroy()
                welcome_screen()

    def clear():
        e_acn.delete(0,"end")
        e_password.delete(0,"end")
        e_acn.focus()
            
    lbl_acn=Label(frm,text="ACCOUNT",font=('arial',13,'bold'),bg='powder blue')
    lbl_acn.place(relx=.32,rely=.1)

    e_acn=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()

    lbl_password=Label(frm,text="PASSWORD",font=('arial',13,'bold'),bg='powder blue')
    lbl_password.place(relx=.31,rely=.2)

    e_password=Entry(frm,font=('arial',15,'bold'),bd=5,show='*')
    e_password.place(relx=.4,rely=.2)

    btn_login=Button(frm,text="Login",font=('arial',15,'bold'),bd=5,command=login)
    btn_login.place(relx=.43,rely=.3)

    btn_clear=Button(frm,text="Clear",font=('arial',15,'bold'),bd=5,command=clear)
    btn_clear.place(relx=.5,rely=.3)

    btn_fp=Button(frm,width=18,text="Forgot Password",font=('arial',15,'bold'),bd=5,command=forgotpassword)
    btn_fp.place(relx=.4,rely=.4)

    btn_new=Button(frm,width=18,text="Open New Account",font=('arial',15,'bold'),bd=5,command=newuser)
    btn_new.place(relx=.4,rely=.5)


def forgotpassword_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    def clear():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()

    def send_otp():
        acn=entry_acn.get()
        email=entry_email.get()

    def forgotpassword_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_email,acn_password from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot password","Record not found")
        else:
            if(tup[0]==email):
                otp=random.randint(1000,9999)
                print(otp)
                try:
                    conobj=gmail.GMail("anjali522@gmail.com","zhme lanc gycw mjkk")
                    msg=gmail.Message(to=email,subject="OTP verification",text=f"your OTP is :{otp}")
                    conobj.send(msg)
                    messagebox.showinfo("password Recovery","OTP sent,check your email")
                except Exception as e:
                    print(e)
                    messagebox.showerror("Password Recovery","Something went wrong") 
        
                lbl_otp=Label(frm,text="otp",bg='powder blue',font=('arial',15,'bold'))
                lbl_otp.place(relx=.7,rely=.45)

                entry_otp=Entry(frm,font=('arial',20,'bold'),bd=5)
                entry_otp.place(relx=.7,rely=.5)
                entry_otp.focus()

                def getpass():
                    verify_otp=int(entry_otp.get())
                    if(otp==verify_otp):
                        messagebox.showinfo("Password Recovery",f"Your Pass:{tup[1]}")
                    else:
                        messagebox.showerror("Password Recovery","Incorrect OTP")
         

                btn_verify=Button(frm,command=getpass,text="verify",font=('arial',20,'bold'),bd=5)
                btn_verify.place(relx=.8,rely=.6)
                    
            else:
                messagebox.showerror("Password Recovery","Email is not correct")
               
        conobj.close()    

    btn_back=Button(frm,text="Back",font=('arial',15,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Account No.",font=('arial',15,'bold'),bg='powder blue')
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()

    lbl_email=Label(frm,text="Email",font=('arial',15,'bold'),bg='powder blue')
    lbl_email.place(relx=.35,rely=.2)

    e_email=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_email.place(relx=.4,rely=.2)

    lbl_mob=Label(frm,text="Mobile No.",font=('arial',15,'bold'),bg='powder blue')
    lbl_mob.place(relx=.31,rely=.3)

    e_mob=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_mob.place(relx=.4,rely=.3)

    btn_otp=Button(frm,command=forgotpassword_db,text="Send OTP",font=('arial',15,'bold'),bd=5)
    btn_otp.place(relx=.6,rely=.4)

    btn_submit=Button(frm,text="Submit",font=('arial',15,'bold'),bd=5,command=forgotpassword_db)
    btn_submit.place(relx=.42,rely=.4)

    btn_clear=Button(frm,text="Clear",font=('arial',15,'bold'),bd=5,command=clear)
    btn_clear.place(relx=.5,rely=.4)

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    def clear():
        e_name.delete(0,"end")
        e_password.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_adhar.delete(0,"end")
        e_address.delete(0,"end")
        cb_gender.delete(0,"end")
        cb_type.delete(0,"end")
        e_name.focus()

    def newuser_db():
        name=e_name.get()
        pwd=e_password.get()
        mob=e_mob.get()
        email=e_email.get()
        adhar=e_adhar.get()
        address=e_address.get()
        gender=cb_gender.get()
        acn_type=cb_type.get()
        bal=0
        opendate=time.strftime("%d %B %Y,%A")

        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("validation","Invalid format of mob")
            return

        match=re.fullmatch(r"[a-zA-Z0-9_]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("validation","Invalid format of email")
            return
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_password,acn_mob,acn_email,acn_bal,acn_opendate,acn_adhar,acn_address,acn_gender,acn_type) values(?,?,?,?,?,?,?,?,?,?)",(name,pwd,mob,email,bal,opendate,adhar,address,gender,acn_type))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()
        messagebox.showinfo("New User",f"Account Created Succesfully with ACN No={tup[0]}")

        e_name.delete(0,"end")
        e_password.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_adhar.delete(0,"end")
        e_address.delete(0,"end")
        cb_gender.delete(0,"end")
        cb_type.delete(0,"end")
        e_name.focus()
        
        

    btn_back=Button(frm,text="Back",font=('arial',15,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text="Name",font=('arial',15,'bold'),bg='powder blue')
    lbl_name.place(relx=.35,rely=.1)

    e_name=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_name.place(relx=.4,rely=.1)
    e_name.focus()

    lbl_password=Label(frm,text="Password",font=('arial',15,'bold'),bg='powder blue')
    lbl_password.place(relx=.32,rely=.2)

    e_password=Entry(frm,font=('arial',15,'bold'),bd=5,show='*')
    e_password.place(relx=.4,rely=.2)

    lbl_mob=Label(frm,text="Mobile No.",font=('arial',15,'bold'),bg='powder blue')
    lbl_mob.place(relx=.31,rely=.3)

    e_mob=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_mob.place(relx=.4,rely=.3)

    lbl_email=Label(frm,text="Email",font=('arial',15,'bold'),bg='powder blue')
    lbl_email.place(relx=.35,rely=.4)

    e_email=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_email.place(relx=.4,rely=.4)

    lbl_adhar=Label(frm,text="Adhar No.",font=('arial',15,'bold'),bg='powder blue')
    lbl_adhar.place(relx=.32,rely=.5)

    e_adhar=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_adhar.place(relx=.4,rely=.5)

    lbl_address=Label(frm,text="Address",font=('arial',15,'bold'),bg='powder blue')
    lbl_address.place(relx=.33,rely=.6)

    e_address=Entry(frm,font=('arial',15,'bold'),bd=5)
    e_address.place(relx=.4,rely=.6)

    lbl_gender=Label(frm,text="Gender",font=('arial',15,'bold'),bg='powder blue')
    lbl_gender.place(relx=.34,rely=.7)

    cb_gender=Combobox(frm,values=['..select..','Male','Female'],font=('arial',18,'bold'))
    cb_gender.place(relx=.4,rely=.7)

    lbl_type=Label(frm,text="Account Type",font=('arial',15,'bold'),bg='powder blue')
    lbl_type.place(relx=.29,rely=.8)

    cb_type=Combobox(frm,values=['..select..','Current','Saving'],font=('arial',18,'bold'))
    cb_type.place(relx=.4,rely=.8)

    btn_submit=Button(frm,text="Submit",font=('arial',15,'bold'),bd=5,command=newuser_db)
    btn_submit.place(relx=.43,rely=.9)

    btn_clear=Button(frm,text="Clear",font=('arial',15,'bold'),bd=5,command=clear)
    btn_clear.place(relx=.54,rely=.9)

def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def logout():
        frm.destroy()
        main_screen()

    def details():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_details=Label(ifrm,text="This is Details screen",font=('arial',18,'bold'),bg='white',fg='blue')
        lbl_details.pack()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_opendate,acn_bal,acn_mob,acn_email,acn_adhar,acn_address from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_name=Label(ifrm,text=f"Name:{tup[0]}",font=('arial',18,'bold'),bg='white')
        lbl_name.place(relx=.2,rely=.22)


        lbl_opendate=Label(ifrm,text=f"Open Date:{tup[1]}",font=('arial',18,'bold'),bg='white')
        lbl_opendate.place(relx=.2,rely=.32)

        lbl_bal=Label(ifrm,text=f"Balance:{tup[2]}",font=('arial',18,'bold'),bg='white')
        lbl_bal.place(relx=.2,rely=.42)

        lbl_mob=Label(ifrm,text=f"Mobile No.:{tup[3]}",font=('arial',18,'bold'),bg='white')
        lbl_mob.place(relx=.2,rely=.52)

        lbl_email=Label(ifrm,text=f"Email:{tup[4]}",font=('arial',18,'bold'),bg='white')
        lbl_email.place(relx=.2,rely=.62)

        lbl_mob=Label(ifrm,text=f"Adhar No.:{tup[5]}",font=('arial',18,'bold'),bg='white')
        lbl_mob.place(relx=.2,rely=.72)

        lbl_email=Label(ifrm,text=f"Address:{tup[6]}",font=('arial',18,'bold'),bg='white')
        lbl_email.place(relx=.2,rely=.82)




    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_password,acn_mob,acn_email from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()


        lbl_update=Label(ifrm,text="This is Update screen",font=('arial',18,'bold'),bg='white')
        lbl_update.pack()

        lbl_name=Label(ifrm,text="Name",font=('arial',15,'bold'),bg='white')
        lbl_name.place(relx=.1,rely=.1)

        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_name.place(relx=.1,rely=.2)
        e_name.insert(0,tup[0])
        e_name.focus()

        lbl_password=Label(ifrm,text="Password",font=('arial',15,'bold'),bg='white')
        lbl_password.place(relx=.1,rely=.4)

        e_password=Entry(ifrm,font=('arial',15,'bold'),bd=5,show='*')
        e_password.place(relx=.1,rely=.5)
        e_password.insert(0,tup[1])

        lbl_mob=Label(ifrm,text="Mobile No.",font=('arial',15,'bold'),bg='white')
        lbl_mob.place(relx=.5,rely=.1)

        e_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_mob.place(relx=.5,rely=.2)
        e_mob.insert(0,tup[2])

        lbl_email=Label(ifrm,text="Email",font=('arial',15,'bold'),bg='white')
        lbl_email.place(relx=.5,rely=.4)

        e_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_email.place(relx=.5,rely=.5)
        e_email.insert(0,tup[3])

        def update_db():
            name=e_name.get()
            pwd=e_password.get()
            mob=e_mob.get()
            email=e_email.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_password=?,acn_mob=?,acn_email=? where acn_no=?",(name,pwd,mob,email,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Record Updated")
            welcome_screen()

        btn_update=Button(ifrm,text="Update",font=('arial',15,'bold'),bd=5,command=update_db)
        btn_update.place(relx=.38,rely=.65)
        
    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_deposit=Label(ifrm,text="This is Deposit screen",font=('arial',18,'bold'),bg='white',fg='blue')
        lbl_deposit.pack()

        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg='white')
        lbl_amt.place(relx=.1,rely=.2)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.3,rely=.2)
        e_amt.focus()

        def deposit_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update",f"{amt} Amount Deposited")

        btn_sub=Button(ifrm,text="Submit",font=('arial',15,'bold'),bd=5,command=deposit_db)
        btn_sub.place(relx=.4,rely=.5)

   
    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_withdraw=Label(ifrm,text="This is withdraw screen",font=('arial',18,'bold'),bg='white',fg='blue')
        lbl_withdraw.pack()

        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg='white')
        lbl_amt.place(relx=.15,rely=.2)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.3,rely=.2)
        e_amt.focus()


        def withdraw_db():
            amt=float(e_amt.get())
  
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("Select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()
            
            if(avail_bal>=amt):
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"{amt} Amount Withdrawn")
            else:
                messagebox.showwarning("Withdraw","Insufficient Bal")

        btn_sub=Button(ifrm,text="Submit",font=('arial',15,'bold'),bd=5,command=withdraw_db)
        btn_sub.place(relx=.4,rely=.5)
        

    def transfer():    
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_transfer=Label(ifrm,text="This is Transfer screen",font=('arial',18,'bold'),bg='white',fg='blue')
        lbl_transfer.pack()

        lbl_amt=Label(ifrm,text="Amount",font=('arial',15,'bold'),bg='white')
        lbl_amt.place(relx=.2,rely=.2)

        e_amt=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_amt.place(relx=.3,rely=.2)
        e_amt.focus()

        lbl_to=Label(ifrm,text="To",font=('arial',15,'bold'),bg='white')
        lbl_to.place(relx=.25,rely=.4)

        e_to=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_to.place(relx=.3,rely=.4)
        e_to.focus()

        def transfer_db():
            to_acn=e_to.get()
            amt=float(e_amt.get())

            if to_acn==gacn:
                messagebox.showwarning("Transfer","To and From can't be same")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("Select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_no from acn where acn_no=?",(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showwarning("Transfer","Invalid To ACN")
                return
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("Update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn))
                curobj.execute("Update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt}transfered to ACN{to_acn} successfully")
  
        btn_sub=Button(ifrm,text="Submit",font=('arial',15,'bold'),bd=5,command=transfer_db)
        btn_sub.place(relx=.4,rely=.6)
        

    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn,))
    tup=curobj.fetchone()
    conobj.close()

    lbl_welcome=Label(frm,text=f"Welcome!,{tup[0]}",font=('arial',18,'bold'),bg='powder blue')
    lbl_welcome.place(relx=0,rely=0)

    btn_logout=Button(frm,text="logout",font=('arial',15,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.9,rely=0)

    btn_details=Button(frm,width=10,text="Details",font=('arial',15,'bold'),bd=5,command=details)
    btn_details.place(relx=0,rely=.1)

    btn_update=Button(frm,width=10,text="Update",font=('arial',15,'bold'),bd=5,command=update)
    btn_update.place(relx=0,rely=.2)

    btn_deposit=Button(frm,width=10,text="Deposit",font=('arial',15,'bold'),bd=5,command=deposit)
    btn_deposit.place(relx=0,rely=.3)

    btn_withdraw=Button(frm,width=10,text="Withdraw",font=('arial',15,'bold'),bd=5,command=withdraw)
    btn_withdraw.place(relx=0,rely=.4)

    btn_transfer=Button(frm,width=10,text="Transfer",font=('arial',15,'bold'),bd=5,command=transfer)
    btn_transfer.place(relx=0,rely=.5)


main_screen()
win.mainloop()


