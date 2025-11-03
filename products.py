from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee import connect_database
import pymysql

def show_all(treeview,search_combobox,search_entry):
    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)
        

def search_product(treeview,search_combobox,search_entry):
    if search_combobox.get()=='Search By':
        messagebox.showwarning('Warning!','Please select an option')
    elif search_entry.get()=='':
        messagebox.showwarning('Warning!','Please enter the value to be searched')
    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute(f'SELECT * from product_data WHERE {search_combobox.get()}=%s',search_entry.get())
        records=cursor.fetchall()
        if len(records)==0:
            messagebox.showerror('Error','No records found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
        
                       
        

def clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    status_combobox.set('Select')

def delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    index = treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    
    ans=messagebox.askyesno('Confirm','Do you want to delete?')
    if ans:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventory_system')
            cursor.execute('DELETE FROM product_data WHERE id=%s',id)
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Info','Record is deleted')
            clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox)
            
        except Exception as e:
                messagebox.showerror('Error', 'Error due {e}')
        finally:
            cursor.close()
            connection.close()

def update_product(category,supplier,name,price,quantity,status,treeview):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    id=content[0]
    if not index:
        messagebox.showerror('Error','No row is selected')
        return
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventory_system')
    cursor.execute('SELECT * from product_data WHERE id=%s',id)
    current_data = cursor.fetchone()
    current_data = current_data[1:]
    current_data=list(current_data)
    current_data[3]=str(current_data[3])
    current_data=tuple(current_data) 
    quantity=int(quantity)
    
    new_data = (category,supplier,name,price,quantity,status)
     
    if current_data==new_data:
        messagebox.showinfo('Info','No Changes detected')
        return
    cursor.execute('UPDATE product_data SET category=%s,supplier=%s,name=%s,price=%s,status=%s,quantity=%s WHERE id=%s',(category,supplier,name,price,quantity,status,id))
    connection.commit()
    messagebox.showinfo('Info','Data is updated')
    treeview_data(treeview)




def select_data(event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    quantity_entry.insert(0,content[5])
    status_combobox.set(content[6])
    

def treeview_data(treeview):
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("Select * from product_data")
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
            
    except Exception as e:
            messagebox.showerror('Error', 'Error due {e}')
    finally:
        cursor.close()
        connection.close()
    

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

def fetch_supplier_category(category_combobox,supplier_combobox):
    category_option=[]
    supplier_option=[]
    cursor,connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute("USE inventory_system")
    cursor.execute("SELECT name from category_data")
    
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)
    
    cursor.execute("SELECT name from supplier_data")
    names=cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)

def add_product(category,supplier,name,price,quantity,status,treeview):
    if category=='Empty':
        messagebox.showerror('Error','Please add categories')
    elif supplier=='Empty':
         messagebox.showerror('Error','Please add suppliers')
    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('Error','All fields are required')
        
    else:
        cursor,connection = connect_database()
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_system")
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),supplier VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2),quantity INT, status VARCHAR(50))')
        cursor.execute('SELECT * from product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error','Product Already Exists')
            return
        
        cursor.execute('INSERT INTO product_data (category,supplier,name,price,quantity,status) VALUES(%s,%s,%s,%s,%s,%s)',(category,supplier,name,price,quantity,status))
        connection.commit()
        messagebox.showinfo('Info','Data is added succesfully')
        treeview_data(treeview)
    

def product_form(window):
   
    product_frame=Frame(window,width=1070,height=567,bg="white")
    product_frame.place(x=200,y=100)
    
    back_button=Button(product_frame,text="Back",font=("times new roman", 15, "bold"),bg="white",fg="black",cursor="hand2",command=lambda:product_frame.place_forget())
    back_button.place(x=10,y=0)
    
    left_frame=Frame(product_frame,bd=3,relief=RIDGE,bg="white")
    left_frame.place(x=20,y=40)
    
    heading_label=Label(left_frame,text="Manage Product Details",font=("times new roman", 20, "bold"),bg="#0f4d7d",fg="white")
    heading_label.grid(row=0,columnspan=20,sticky='w',padx=135)
    
    id_label=Label(left_frame,text="Id",font=("times new roman", 15, "bold"),bg="white")
    id_label.grid(row=1,column=0,padx=20,sticky="w")
    
    category_label=Label(left_frame,text="Category",font=("times new roman", 15, "bold"),bg="white")
    category_label.grid(row=1,column=0,padx=20,sticky="w")
    category_combobox=ttk.Combobox(left_frame,font=("times new roman", 15, "bold"))
    category_combobox.grid(row=1,column=1,pady=40)
    category_combobox.set('Empty')
    
    supplier_label=Label(left_frame,text="Supplier",font=("times new roman", 15, "bold"),bg="white")
    supplier_label.grid(row=2,column=0,padx=20,sticky="w")
    supplier_combobox=ttk.Combobox(left_frame,font=("times new roman", 15, "bold"))
    supplier_combobox.grid(row=2,column=1)
    supplier_combobox.set('Empty')
    
    name_label=Label(left_frame,text="Name",font=("times new roman", 15, "bold"),bg="white")
    name_label.grid(row=3,column=0,padx=20,sticky='w')
    
    name_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    name_entry.grid(row=3,column=1,pady=40)
    
    price_label=Label(left_frame,text="Price",font=("times new roman", 15, "bold"),bg="white")
    price_label.grid(row=4,column=0,padx=20,sticky='w')
    
    price_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    price_entry.grid(row=4,column=1,pady=0)
    '''
    discount_label=Label(left_frame,text='Discount(%s)',font=("times new roman", 15),bg="lightyellow")
    discount_label.grid(row=5,column=0,padx=20,sticky='w',pady=(20,0))
    discount_spinbox = Spinbox(left_frame,from_=0, to=100,font=("times new roman", 15))
    discount_spinbox.grid(row=5,column=1,pady=(20,0))'''
    
    quantity_label=Label(left_frame,text="Quantity",font=("times new roman", 15, "bold"),bg="white")
    quantity_label.grid(row=5,column=0,padx=20,sticky='w')
    
    quantity_entry=Entry(left_frame,font=("times new roman", 15),bg="lightyellow")
    quantity_entry.grid(row=5,column=1,pady=30)
    
    status_label=Label(left_frame,text="Status",font=("times new roman", 15, "bold"),bg="white")
    status_label.grid(row=7,column=0,padx=20,sticky="w")
    
    status_combobox=ttk.Combobox(left_frame, values=('Active','Inactive'),font=("times new roman", 15))
    status_combobox.grid(row=7,column=1)
    status_combobox.set('Select Status')
    
    button_frame = Frame(left_frame,bg='white')
    button_frame.grid(row=8,columnspan=2,pady=(30,10))
    
    add_button=Button(button_frame,text="Add",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:add_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    add_button.grid(row=0,column=0,padx=10)
    
    update_button=Button(button_frame,text="Update",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:update_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0,column=1,padx=10)
    
    delete_button=Button(button_frame,text="Delete",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    delete_button.grid(row=0,column=2,padx=20)
    
    clear_button=Button(button_frame,text="Clear",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,treeview))
    clear_button.grid(row=0,column=3,padx=20)
    
    search_frame = LabelFrame(product_frame,text='Search Product',font=("times new roman", 15))
    search_frame.place(x=600,y=40)
    
    search_combobox=ttk.Combobox(search_frame, values=('Category','Supplier','Name','Status'),state='readonly',width=16,font=("times new roman", 15))
    search_combobox.grid(row=0,column=0)
    search_combobox.set('Search By')
    
    search_entry=Entry(search_frame,font=("times new roman", 15),bg="lightyellow",width=16)
    search_entry.grid(row=0,column=1)
    
    search_button=Button(search_frame,text="Search",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:search_product(treeview,search_combobox,search_entry))
    search_button.grid(row=7,column=2,padx=(10,10),pady=0)
    
    show_button=Button(search_frame,text="Show",font=("times new roman", 15),bg="#0f4d7d",fg="white",cursor='hand2',width=8,command=lambda:show_all(treeview,search_combobox,search_entry))
    show_button.grid(row=7,column=0)
    
    treeview_frame = Frame(product_frame,bg='lightyellow')
    treeview_frame.place(x=590,y=150,width=470,height=420)
    
    scroly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrolx=Scrollbar(treeview_frame,orient=HORIZONTAL)

    treeview=ttk.Treeview(treeview_frame,columns=("id","category","name","supplier","price","quantity",'status'),yscrollcommand=scroly.set,xscrollcommand=scrolx.set)
    scroly.pack(side=RIGHT,fill=Y)
    scrolx.pack(side=BOTTOM,fill=X)
    scroly.config(command=treeview.yview)
    scrolx.config(command=treeview.xview)
    treeview.pack(fill=BOTH,expand=1)
    
    treeview.heading("id",text="ID")
    treeview.heading("category",text="Category")
    treeview.heading("name",text="Product Name")
    treeview.heading("supplier",text="Supplier")
    treeview.heading("price",text="Price")
    treeview.heading("quantity",text="Quantity")
    treeview.heading("status",text="Status")
    treeview_data(treeview)
    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    return product_frame
    
connect_database()
    
    
    
    