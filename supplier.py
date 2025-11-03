from tkinter import *
from tkinter import ttk, messagebox
import os
from employee import connect_database
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
    
def delete_supplier(invoice,treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s',invoice)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info','Record is deleted')
        
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()
    
    
def clear(invoice_entry,name_entry,contact_entry,description_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())
    
    
def search_supplier(search_value,treeview):
    if search_value=='':
        messagebox.showerror('Error','Please enter invoice no')
    else:
        cursor,connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s',search_value)
        record=cursor.fetchone()
        if not record:
            messagebox.showerror('Error','No record found')
            
        treeview.delete(*treeview.get_children())
        treeview.insert('',END,values=record)
        
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
            return
    finally:
        cursor.close()
        connection.close()
        
def show_all(treeview,search_entrys):
    treeview_data(treeview)
    search_entrys.delete(0,END)
    
def update_supplier(invoice,name,contact,description,treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * from supplier_data WHERE invoice=%s',invoice)
        current_data = cursor.fetchone()
        current_data = current_data[1:]
        print(current_data)
        
        
        new_data = (name,contact,description)
        print(new_data)
        
        if current_data==new_data:
            messagebox.showinfo('Info','No Changes detected')
        
        
        cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,description=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('Info','Data is updated')
        treeview_data(treeview)
    
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()
    
    
    
def select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    
    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])


def treeview_data(treeview):
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("Select * from supplier_data")
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
            
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()

def add_supplier(invoice,name,contact,description,treeview):
    if invoice=="" or name=="" or contact=="" or description =="":
        messagebox.showerror("Error","ALL fields are required")
        return
    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute("Use inventory_system")
            cursor.execute("SELECT * from supplier_data WHERE invoice=%s",invoice)
            
            if cursor.fetchone():
             messagebox.showerror('Error','ID Already exists')
            cursor.execute("CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY,name VARCHAR(100),contact VARCHAR(15),description TEXT)")

            cursor.execute("INSERT INTO supplier_data VALUES(%s,%s,%s,%s)",(invoice,name,contact,description))
            connection.commit()
            messagebox.showinfo("Success","Supplier added successfully")
            treeview_data(treeview)
            
        except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
        finally:
            cursor.close()
            connection.close()
    


def supplier_form(window):
    supplier_frame=Frame(window,width=1070,height=567,bg="white")
    supplier_frame.place(x=200,y=100)

    heading_label=Label(supplier_frame,text="Manage Supplier Details",font=("times new roman", 20, "bold"),bg="#0f4d7d",fg="white")
    heading_label.place(x=0,y=0,relwidth=1)

    back_button=Button(supplier_frame,text="Back",font=("times new roman", 15, "bold"),bg="white",fg="black",cursor="hand2",command=lambda:supplier_frame.destroy())
    back_button.place(x=10,y=40)

    left_frame=Frame(supplier_frame,bd=3,relief=RIDGE,bg="white")
    left_frame.place(x=10,y=100,width=500,height=470)

    invoice_label=Label(left_frame,text="Invoice No.",font=("times new roman", 15, "bold"),bg="white")
    invoice_label.grid(row=0,column=0,padx=(20,40),pady=10,sticky="w")
    invoice_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    invoice_entry.grid(row=0,column=1,padx=10,pady=10,sticky="w")
    
    name_label=Label(left_frame,text="Supplier Name",font=("times new roman", 15, "bold"),bg="white")
    name_label.grid(row=1,column=0,padx=(20,40),pady=10,sticky="w")
    name_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    name_entry.grid(row=1,column=1,padx=10,pady=10,sticky="w")

    contact_label=Label(left_frame,text="Supplier Contact",font=("times new roman", 15, "bold"),bg="white")
    contact_label.grid(row=2,column=0,padx=(20,40),pady=10,sticky="w")
    contact_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    contact_entry.grid(row=2,column=1,padx=10,pady=10,sticky="w")

    description_label=Label(left_frame,text="Description",font=("times new roman", 15, "bold"),bg="white")
    description_label.grid(row=3,column=0,padx=(20,40),pady=10,sticky="nw")
    description_text=Text(left_frame,font=("times new roman", 15),bg="lightyellow",width=25,height=6,bd=2,relief=RIDGE)
    description_text.grid(row=3,column=1,padx=10,pady=10,sticky="w")


    button_frame=Frame(left_frame,bg="white")
    button_frame.grid(row=4,columnspan=2)

    add_button=Button(button_frame,text="Add",font=("times new roman", 15, "bold"),bg="#2196f3",fg="white",cursor="hand2",width=7,command=lambda :add_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=15,pady=10)

    update_button=Button(button_frame,text="Update",font=("times new roman", 15, "bold"),bg="#4caf50",fg="white",cursor="hand2",width=7,command=lambda:update_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1,pady=10)

    delete_button=Button(button_frame,text="Delete",font=("times new roman", 15, "bold"),bg="#f44336",fg="white",cursor="hand2",width=7,command=lambda :delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=15,pady=10)

    clear_button=Button(button_frame,text="Clear",font=("times new roman", 15, "bold"),bg="#607d8b",fg="white",cursor="hand2",width=7,command=lambda: clear(invoice_entry,name_entry,contact_entry,description_text,treeview))
    clear_button.grid(row=0,column=3,pady=10)


    right_frame=Frame(supplier_frame,bd=3,relief=RIDGE,bg="white")
    right_frame.place(x=520,y=100,width=500,height=350)

    search_frame=Frame(right_frame,bg="white")
    search_frame.pack()

    invoice_label=Label(search_frame,text="Invoice No.",font=("times new roman", 15, "bold"),bg="white")
    invoice_label.grid(row=0,column=0,padx=10,pady=10,sticky="w")
    search_entrys=Entry(search_frame,font=("times new roman", 15),bg="lightyellow",width=15)
    search_entrys.grid(row=0,column=1,padx=10,pady=10,sticky="w")

    search_button=Button(search_frame,text="Search",font=("times new roman", 15),bg="#03a9f4",fg="white",cursor="hand2",width=7,command=lambda :search_supplier(search_entrys.get(),treeview))
    search_button.grid(row=0,column=2,padx=10,pady=10)
    showall_button=Button(search_frame,text="Show all",font=("times new roman", 15),bg="#03a9f4",fg="white",cursor="hand2",width=7,command=lambda :show_all(treeview,search_entrys))
    showall_button.grid(row=0,column=3,padx=10,pady=10)

    scroly=Scrollbar(right_frame,orient=VERTICAL)
    scrolx=Scrollbar(right_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(right_frame,columns=("invoice","name","contact","description"),yscrollcommand=scroly.set,xscrollcommand=scrolx.set)
    scroly.pack(side=RIGHT,fill=Y)
    scrolx.pack(side=BOTTOM,fill=X)
    scroly.config(command=treeview.yview)
    scrolx.config(command=treeview.xview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.heading("invoice",text="Invoice No.")
    treeview.heading("name",text="Supplier Name")
    treeview.heading("contact",text="Supplier Contact")
    treeview.heading("description",text="Description")
    treeview["show"]="headings"

    treeview.column("invoice",width=80)
    treeview.column("name",width=160)
    treeview.column("contact",width=120)
    treeview.column("description",width=300)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview))

create_database_table()
connect_database()