from tkinter import *
from tkinter import messagebox
import os
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql


def connect_database():
    try:
        connection=pymysql.connect(host="localhost",user="root",password="dev@123") # your password
        #{key:dets}
        #dict.get(key,notfound)
        cursor=connection.cursor()
    except:
        messagebox.showerror("Error","Invalid Details, Please try again,please open mysql command line client")
        return None, None
    return cursor,connection

def create_database_table():
    cursor,connection = connect_database()
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
    cursor.execute("USE inventory_system")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS employee_data("
        "empid INT PRIMARY KEY AUTO_INCREMENT,"
        "name VARCHAR(100),"
        "email VARCHAR(100),"
        "gender VARCHAR(50),"
        "dob VARCHAR(30),"
        "contact VARCHAR(30),"
        "employement_type VARCHAR(50),"
        "education VARCHAR(50),"
        "work_shift VARCHAR(50),"
        "address TEXT,"
        "doj VARCHAR(30),"
        "salary VARCHAR(50),"
        "usertype VARCHAR(50),"
        "password VARCHAR(50)"
        ")"
    )

create_database_table()
connect_database()

def treeview_data():
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute("USE inventory_system")
    try:
        cursor.execute("SELECT * FROM employee_data")
        employee_records = cursor.fetchall()
        # print(employee_records)
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror("Error",f"Error fetching data: {e}")
    finally:
        cursor.close()
        connection.close()



def clear_fields(empid_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, employement_type_combobox,
                 education_combobox, work_shift_combobox, address_text, doj_entry, salary_entry, usertype_combobox, password_entry,check=None):
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    gender_combobox.set("Select")
    from datetime import date
    dob_entry.set_date(date.today())
    contact_entry.delete(0, END)
    employement_type_combobox.set("Select")
    contact_entry.delete(0, END)
    education_combobox.set("Select")
    work_shift_combobox.set("Select")
    address_text.delete("1.0", END)
    doj_entry.set_date(date.today())
    salary_entry.delete(0, END)
    usertype_combobox.set("Select")
    password_entry.delete(0, END)
    if check:
       employee_treeview.selection_remove(employee_treeview.selection())



def update_employee(empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password):
    selected_item = employee_treeview.selection()
    
    if not selected_item:
        messagebox.showerror("Error", "No employee selected for update")
        return
    try:
        cursor,connection= connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_system")
        cursor.execute("SELECT * FROM employee_data WHERE empid=%s", (empid,))
        current_record = cursor.fetchone()
        current_record = current_record[1:]  # Exclude empid from comparison

        address=address.strip()

        new_record=(name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password)

        if current_record == new_record:
            messagebox.showinfo("Info", "No changes detected to update")
            return
        cursor.execute("UPDATE employee_data SET name=%s,email=%s,gender=%s,dob=%s,contact=%s,employement_type=%s,"
                        "education=%s,work_shift=%s,address=%s,doj=%s,salary=%s,usertype=%s,password=%s WHERE empid=%s",
                        (name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password, empid))
        connection.commit()
        treeview_data()
        messagebox.showinfo("Success", "Employee details updated successfully")
        
    except Exception as e:
            messagebox.showerror("Error", f"Error updating employee: {e}")
    
    finally:
            cursor.close()
            connection.close()
                       



def select_data(event=None, empid_entry=None, name_entry=None, email_entry=None, gender_combobox=None, dob_entry=None,
                contact_entry=None, employement_type_combobox=None, education_combobox=None, work_shift_combobox=None,
                address_text=None, doj_entry=None, salary_entry=None, usertype_combobox=None, password_entry=None,check=None):
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    # print(row)
    clear_fields(empid_entry, name_entry, email_entry, gender_combobox, dob_entry,
                 contact_entry, employement_type_combobox, education_combobox, work_shift_combobox,
                 address_text, doj_entry, salary_entry, usertype_combobox, password_entry)
    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gender_combobox.set(row[3])
    dob_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    employement_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert("1.0",row[9])
    doj_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0,row[13])


def add_employee(empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password):
    if empid=="" or name=="" or email=="" or gender=="Select" or contact=="" or employement_type=="Select" or education=="Select" or work_shift=="Select" or address=="\n" or salary=="" or usertype=="Select" or password=="":
        messagebox.showerror("Error","All fields are required")
        return
    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_system") 
        try:
            cursor.execute("SELECT empid FROM employee_data WHERE empid=%s", (empid,))
            if cursor.fetchone():
                messagebox.showerror("Error","Employee ID already exists")
                return
            address=address.strip()
            cursor.execute("INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success","Employee added successfully")
        except Exception as e:
            messagebox.showerror("Error",f"Error adding employee: {e}")
        finally:
            cursor.close()
            connection.close()



def delete_employee(empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, usertype, password):
    selected_item = employee_treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "No employee selected for deletion")
        return
    empid = employee_treeview.item(selected_item)['values'][0]
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete employee ID {empid}?")
    if confirm:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_system")
        try:
            cursor.execute("DELETE FROM employee_data WHERE empid=%s", (empid,))
            connection.commit()
            treeview_data()
            messagebox.showinfo("Success", "Employee deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting employee: {e}")
        finally:
            cursor.close()
            connection.close()


def search_employee(search_option,value):
    if search_option=="Search By":
        messagebox.showerror("Error","Select a valid option to search")
        return
    if value=="":
        messagebox.showerror("Error","Search input is required")
        return
    
    search_option=search_option.replace(" ","_")
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute("USE inventory_system")
    try:
        query = f"SELECT * FROM employee_data WHERE {search_option.lower()} LIKE %s"
        cursor.execute(query, (f"%{value}%",))
        employee_records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        
        for record in employee_records:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror("Error", f"Error searching employee: {e}")
    finally:
        cursor.close()
        connection.close()


def show_all_employees(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set("Search By")



def employee_form(window):
    global employee_treeview
    employee_frame=Frame(window,width=1070,height=567)
    employee_frame.place(x=200,y=100)
    heading_label=Label(employee_frame,text="Manage Employee Details",font=("times new roman", 20, "bold"),bg="#0f4d7d",fg="white")
    heading_label.place(x=0,y=0,relwidth=1)

    top_frame=Frame(employee_frame,bg="white")
    top_frame.place(x=0,y=40,relwidth=1,height=235)

    back_button=Button(top_frame,text="Back",font=("times new roman", 15, "bold"),bg="white",fg="black",cursor="hand2",command=lambda:employee_frame.destroy())
    back_button.place(x=10,y=0)

    search_frame=Frame(top_frame,bg="white")
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=("Empid","Name","Email","education","work shift"),font=("times new roman", 15),state="readonly",width=15)
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set("Search By")
    search_entry=Entry(search_frame,font=("times new roman", 15),width=20,bg="lightyellow")
    search_entry.grid(row=0,column=1,padx=10)
    search_button=Button(search_frame,text="Search",font=("times new roman", 15),bg="#03a9f4",fg="white",cursor="hand2",command=lambda:search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0,column=2,padx=10)
    showall_button=Button(search_frame,text="Show all",font=("times new roman", 15),bg="#03a9f4",fg="white",cursor="hand2",command=lambda:show_all_employees(search_entry,search_combobox))
    showall_button.grid(row=0,column=3,padx=10)


    horizontal_scroll=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scroll=Scrollbar(top_frame,orient=VERTICAL)
    employee_treeview=ttk.Treeview(top_frame,columns=("empid","name","email","gender","dob","contact","employement_type","education","work_shift","address","doj","salary","usertype"),show="headings",
                                   yscrollcommand=vertical_scroll.set,xscrollcommand=horizontal_scroll.set)
    horizontal_scroll.pack(side=BOTTOM,fill=X)
    vertical_scroll.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scroll.config(command=employee_treeview.xview)
    vertical_scroll.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10,0))

    employee_treeview.heading("empid",text="Emp ID")
    employee_treeview.heading("name",text="Name")
    employee_treeview.heading("email",text="Email")
    employee_treeview.heading("gender",text="Gender")
    employee_treeview.heading("dob",text="Date of Birth")
    employee_treeview.heading("contact",text="Contact")
    employee_treeview.heading("employement_type",text="Employement Type")
    employee_treeview.heading("education",text="Education")
    employee_treeview.heading("work_shift",text="Work Shift")
    employee_treeview.heading("address",text="Address")
    employee_treeview.heading("doj",text="Date of Joining")
    employee_treeview.heading("salary",text="Salary")
    employee_treeview.heading("usertype",text="User Type")

    treeview_data()
    employee_treeview.bind("<ButtonRelease-1>",lambda event:select_data(event,empid_entry, name_entry, email_entry, gender_combobox, dob_entry,
                                                                         contact_entry, employement_type_combobox,education_combobox, work_shift_combobox,
                                                                           address_text, doj_entry, salary_entry, usertype_combobox, password_entry))



    employee_treeview.column("empid",width=80)
    employee_treeview.column("name",width=140)
    employee_treeview.column("email",width=180)
    employee_treeview.column("gender",width=80)
    employee_treeview.column("dob",width=100)
    employee_treeview.column("contact",width=100)
    employee_treeview.column("employement_type",width=120)
    employee_treeview.column("education",width=120)
    employee_treeview.column("work_shift",width=100)
    employee_treeview.column("address",width=200)
    employee_treeview.column("doj",width=100)
    employee_treeview.column("salary",width=140)
    employee_treeview.column("usertype",width=120)

    detail_frame=Frame(employee_frame)
    detail_frame.place(x=30,y=280)

    empid_label=Label(detail_frame,text="Emp ID",font=("times new roman", 12),bg="white")
    empid_label.grid(row=0,column=0,padx=10,pady=10,sticky="w")
    empid_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    empid_entry.grid(row=0,column=1,padx=10,pady=10,sticky="w")

    name_label=Label(detail_frame,text="Name",font=("times new roman", 12),bg="white")
    name_label.grid(row=0,column=2,padx=10,pady=10,sticky="w")
    name_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    name_entry.grid(row=0,column=3,padx=10,pady=10,sticky="w")

    email_label=Label(detail_frame,text="Email",font=("times new roman", 12),bg="white")
    email_label.grid(row=0,column=4,padx=10,pady=10,sticky="w")
    email_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    email_entry.grid(row=0,column=5,padx=10,pady=10,sticky="w")

    gender_label=Label(detail_frame,text="Gender",font=("times new roman", 12),bg="white")
    gender_label.grid(row=1,column=0,padx=10,pady=10,sticky="w")
    gender_combobox=ttk.Combobox(detail_frame,values=("Male","Female","Other"),font=("times new roman", 12),state="readonly",width=20)
    gender_combobox.grid(row=1,column=1,padx=10,pady=10,sticky="w")
    gender_combobox.set("Select")

    dob_label=Label(detail_frame,text="Date of Birth",font=("times new roman", 12),bg="white")
    dob_label.grid(row=1,column=2,padx=10,pady=10,sticky="w")
    dob_entry=DateEntry(detail_frame,font=("times new roman", 12),width=20,bg="lightyellow",date_pattern="dd-mm-yyyy",state="readonly")
    dob_entry.grid(row=1,column=3,padx=10,pady=10,sticky="w")

    contact_label=Label(detail_frame,text="Contact",font=("times new roman", 12))
    contact_label.grid(row=1,column=4,padx=10,pady=10,sticky="w")
    contact_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    contact_entry.grid(row=1,column=5,padx=10,pady=10,sticky="w")

    employement_type_label=Label(detail_frame,text="Employement Type",font=("times new roman", 12),bg="white")
    employement_type_label.grid(row=2,column=0,padx=10,pady=10,sticky="w")
    employement_type_combobox=ttk.Combobox(detail_frame,values=("Full Time","Part Time","Contract","Casual","Intern"),font=("times new roman", 12),state="readonly",width=20)
    employement_type_combobox.grid(row=2,column=1,padx=10,pady=10,sticky="w")
    employement_type_combobox.set("Select") 

    education_label=Label(detail_frame,text="Education",font=("times new roman", 12),bg="white")
    education_label.grid(row=2,column=2,padx=10,pady=10,sticky="w")
    education_combobox=ttk.Combobox(detail_frame,values=("High School","Diploma","Bachelor's","Master's","PhD","B-Tech","M-Tech"),font=("times new roman", 12),state="readonly",width=20)
    education_combobox.grid(row=2,column=3,padx=10,pady=10,sticky="w")
    education_combobox.set("Select")

    work_shift_label=Label(detail_frame,text="Work Shift",font=("times new roman", 12),bg="white")
    work_shift_label.grid(row=2,column=4,padx=10,pady=10,sticky="w")
    work_shift_combobox=ttk.Combobox(detail_frame,values=("Morning","Evening","Night"),font=("times new roman", 12),state="readonly",width=20)
    work_shift_combobox.grid(row=2,column=5,padx=10,pady=10,sticky="w")
    work_shift_combobox.set("Select")

    address_label=Label(detail_frame,text="Address",font=("times new roman", 12),bg="white")
    address_label.grid(row=3,column=0,padx=10,pady=10,sticky="w")
    address_text=Text(detail_frame,font=("times new roman", 12),width=20,height=3,bg="lightyellow")
    address_text.grid(row=3,column=1,padx=10,pady=10,sticky="w",rowspan=2)

    doj_label=Label(detail_frame,text="Date of Joining",font=("times new roman", 12),bg="white")
    doj_label.grid(row=3,column=2,padx=10,pady=10,sticky="w")
    doj_entry=DateEntry(detail_frame,font=("times new roman", 12),width=20,bg="lightyellow",date_pattern="dd-mm-yyyy",state="readonly")
    doj_entry.grid(row=3,column=3,padx=10,pady=10,sticky="w")

    salary_label=Label(detail_frame,text="Salary",font=("times new roman", 12),bg="white")
    salary_label.grid(row=3,column=4,padx=10,pady=10,sticky="w")
    salary_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    salary_entry.grid(row=3,column=5,padx=10,pady=10,sticky="w")

    usertype_label=Label(detail_frame,text="User Type",font=("times new roman", 12),bg="white")
    usertype_label.grid(row=4,column=2,padx=10,pady=10,sticky="w")
    usertype_combobox=ttk.Combobox(detail_frame,values=("Admin","Employee"),font=("times new roman", 12),state="readonly",width=20)
    usertype_combobox.grid(row=4,column=3,padx=10,pady=10,sticky="w")
    usertype_combobox.set("Select") 

    password_label=Label(detail_frame,text="Password",font=("times new roman", 12),bg="white")
    password_label.grid(row=4,column=4,padx=10,pady=10,sticky="w")
    password_entry=Entry(detail_frame,font=("times new roman", 12),width=22,bg="lightyellow")
    password_entry.grid(row=4,column=5,padx=10,pady=10,sticky="w")

    button_frame=Frame(employee_frame,bg="white")
    button_frame.place(x=200,y=510)

    add_button=Button(button_frame,text="Add",font=("times new roman", 15),bg="#03a9f4",fg="white",cursor="hand2",width=10,command=lambda:add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),dob_entry.get(),contact_entry.get(),employement_type_combobox.get(),
                                                                                                                                                education_combobox.get(),work_shift_combobox.get(),address_text.get("1.0",END),doj_entry.get(),salary_entry.get(),usertype_combobox.get(),
                                                                                                                                                password_entry.get()))
    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text="Update",font=("times new roman", 15),bg="#4caf50",fg="white",cursor="hand2",width=10,command=lambda:update_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),dob_entry.get(),contact_entry.get(),employement_type_combobox.get(),
                                                                                                                                                education_combobox.get(),work_shift_combobox.get(),address_text.get("1.0",END),doj_entry.get(),salary_entry.get(),usertype_combobox.get(),
                                                                                                                                                password_entry.get()))
    update_button.grid(row=0,column=1,padx=20)

    delete_button=Button(button_frame,text="Delete",font=("times new roman", 15),bg="#f44336",fg="white",cursor="hand2",width=10,command=lambda:delete_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),dob_entry.get(),contact_entry.get(),employement_type_combobox.get(),
                                                                                                                                                education_combobox.get(),work_shift_combobox.get(),address_text.get("1.0",END),doj_entry.get(),salary_entry.get(),usertype_combobox.get(),
                                                                                                                                                password_entry.get()))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text="Clear",font=("times new roman", 15),bg="#607d8b",
                        fg="white",cursor="hand2",width=10,command=lambda : clear_fields(empid_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, employement_type_combobox,
                                                                                                  education_combobox, work_shift_combobox, address_text, doj_entry, salary_entry, usertype_combobox, password_entry,check=True))
    clear_button.grid(row=0,column=3,padx=20)
    create_database_table()