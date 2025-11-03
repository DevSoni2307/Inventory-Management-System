from tkinter import *
import os
from tkinter import ttk, messagebox
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

connect_database()

def treeview_data(treeview):
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("Select * from category_data")
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
            
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()
        
def delete_category(treeview):
    index = treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id=%s',id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Info','Record is deleted')
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()
    
        
def clear(id_entry,category_name_entry,description_text):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)
        

def add_category(id,name,description,treeview):
    if id=='' or name=='' or description=='':
        messagebox.showerror("Error","ALL fields are required")
    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute("CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY,name VARCHAR(100),description TEXT)")
            cursor.execute('SELECT * from category_data WHERE id=%s',id)
            if cursor.fetchone():
                messagebox.showerror('Error','Id already exists')
                return
            cursor.execute('INSERT INTO category_data VALUES(%s,%s,%s)',(id,name,description))
            connection.commit()
            messagebox.showinfo('Info','Data is inserted')
            treeview_data(treeview)
            
        except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
        finally:
            cursor.close()
            connection.close()
        

def category_form(window):
    global logo,product_category_icon
    category_frame=Frame(window,width=1070,height=567,bg="white")
    category_frame.place(x=200,y=100)
    
    heading_label=Label(category_frame,text="Manage category Details",font=("times new roman", 20, "bold"),bg="#0f4d7d",fg="white")
    heading_label.place(x=0,y=0,relwidth=1)
     
    back_button=Button(category_frame,text="Back",font=("times new roman", 15, "bold"),bg="white",fg="black",cursor="hand2",command=lambda:category_frame.place_forget())
    back_button.place(x=10,y=40)
    
    '''
    script_dir = os.path.dirname(os.path.abspath(__file__))
    product_category_img = os.path.join(script_dir,'product_category.png')
    product_category_icon = PhotoImage(file=product_category_img)
    logo = PhotoImage(file=product_category_icon)
    label = Label(category_frame,image = logo,bg='white')
    label.place(x=30,y=100)
    '''
    
    details_frame = Frame(category_frame,bg='white')
    details_frame.place(x=500,y=60)
    
    id_label=Label(details_frame,text="ID",font=("times new roman", 15, "bold"),bg="white")
    id_label.grid(row=0,column=0,padx=20,sticky="w")
    id_entry=Entry(details_frame,font=("times new roman", 15),bg="lightyellow")
    id_entry.grid(row=0,column=1)
    
    category_name_label=Label(details_frame,text="Category Name",font=("times new roman", 15, "bold"),bg="white")
    category_name_label.grid(row=1,column=0,padx=20,sticky="w")
    category_name_entry=Entry(details_frame,font=("times new roman", 15),bg="lightyellow")
    category_name_entry.grid(row=1,column=1,pady=20)
    
    description_label=Label(details_frame,text="Description",font=("times new roman", 15, "bold"),bg="white")
    description_label.grid(row=2,column=0,padx=20,sticky="w")
    
    description_text=Text(details_frame,font=("times new roman", 15),bg="lightyellow",width=25,height=6,bd=2,relief=RIDGE)
    description_text.grid(row=2,column=1,pady=25)
    
    button_frame = Frame(category_frame,bg='white')
    button_frame.place(x=580,y=280)
    
    add_button=Button(button_frame,text="Add",font=("times new roman", 15, "bold"),bg="#0f4d7d",fg="white",cursor="hand2",width=7,command=lambda :add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)
    
    delete_button=Button(button_frame,text="Delete",font=("times new roman", 15, "bold"),bg="#0f4d7d",fg="white",cursor="hand2",width=7,command=lambda:delete_category(treeview))
    delete_button.grid(row=0,column=1,padx=25,pady=15)
    
    clear_button=Button(button_frame,text="Clear",font=("times new roman", 15, "bold"),bg="#0f4d7d",fg="white",cursor="hand2",width=7,command=lambda:clear(id_entry,category_name_entry,description_text))
    clear_button.grid(row=0,column=2,padx=25,pady=15)
    
    treeview_frame = Frame(category_frame,bg='yellow')
    treeview_frame.place(x=530,y=340,height=200,width=500)
    
    scroly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrolx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=('id','name','description'),yscrollcommand=scroly.set,xscrollcommand=scrolx.set)
    scroly.pack(side=RIGHT,fill=Y)
    scrolx.pack(side=BOTTOM,fill=X)
    scroly.config(command=treeview.yview)
    scrolx.config(command=treeview.xview)
    treeview.pack(fill=BOTH,expand=1)
    
    treeview.heading("id",text="ID")
    treeview.heading("name",text="Category Name")
    treeview.heading("description",text="Description")
    
    treeview.column("id",width=80)
    treeview.column("name",width=140)
    treeview.column("description",width=300)
    treeview_data(treeview)


















