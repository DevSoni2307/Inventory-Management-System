from tkinter import *
import os
from employee import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from employee import connect_database
from tkinter import ttk, messagebox
import pymysql,time

def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    cursor.execute('use inventory_system')
    
    cursor.execute('SELECT * from employee_data')
    emp_records=cursor.fetchall()
    total_emp_count_label.config(text=len(emp_records))
    
    cursor.execute('SELECT * from supplier_data')
    sup_records=cursor.fetchall()
    total_sup_count_label.config(text=len(sup_records))
    
    cursor.execute('SELECT * from category_data')
    cat_records=cursor.fetchall()
    total_cat_count_label.config(text=len(cat_records))
    
    cursor.execute('SELECT * from product_data')
    prod_records=cursor.fetchall()
    total_pdt_count_label.config(text=len(prod_records))
    
    date_time = time.strftime('%A:%I:%M:%S %p on %A, %B, %d, %Y')
    subtitlelabel.config(text=f'Welcome Admin\t\t {date_time}')
    subtitlelabel.after(1000,update)
    print(date_time)


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

current_frame = None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)
    
    
def tax_window():
    def save_tax():
        value = tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT primary key,tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1',value)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES(1,%s)',value)
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set too {value} and saved successfully',parent=tax_root)
        
    tax_root=Toplevel()
    tax_root.title('Tax Window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text='Enter Tax Percentage(%)',font=('arial',12))
    tax_percentage.pack()
    tax_count=Spinbox(tax_root,from_=0,to=100,font=('arial',12))
    tax_count.pack(pady=10)
    save_button = Button(tax_root,text='Save',font=('arial',12,'bold'),bg='#4d636d',fg='white',width=10,command=lambda:save_tax())
    save_button.pack(pady=20)
    

# GUI Part
window = Tk()

window.title("Dashboard")
window.geometry("1270x675+0+0")
window.config(bg="white")
window.resizable(True, True)

# Build an absolute path to the image so this works even if the script is
# executed from a different working directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "inventory (1).png")

# Create PhotoImage correctly and keep a reference to it so Tcl/Tk doesn't
# garbage-collect the image (which would make it disappear from the UI).
bg_image = PhotoImage(file=img_path)

titlelabel = Label(window,image=bg_image,compound=LEFT,text="  Inventory Management System",font=("times new roman", 40, "bold"),bg="#010c48",fg="white",anchor="w",padx=20,)
titlelabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window,text="Logout",font=("times new roman", 20, "bold"),fg="#010c48",)
logoutButton.place(x=1100, y=10)

subtitlelabel = Label(window,text="Welcome Admin\t\t Date: 12-10-2025\t\t Time: 12:24:17 am",font=("times new roman", 15, "bold"),bg="#4d636d",fg="white")
subtitlelabel.place(x=0, y=70,relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0,y=102,width=200,height=555)

script_dir = os.path.dirname(os.path.abspath(__file__))
img_path1 = os.path.join(script_dir, "logo.png")

logoimage= PhotoImage(file=img_path1)
imageLabel = Label(leftFrame,image=logoimage)
imageLabel.pack(fill=X) 

menuLabel = Label(leftFrame,text="Menu",font=("times new roman", 20, "bold"),bg="#009688")
menuLabel.pack(fill=X)

img_path2 = os.path.join(script_dir, "man.png")
employee_icon= PhotoImage(file=img_path2)

employee_Button = Button(leftFrame,image=employee_icon, compound=LEFT,text=" Employees",font=("times new roman", 20, "bold"),anchor="w",command=lambda:show_form(employee_form))
employee_Button.pack(fill=X)

img_path3 = os.path.join(script_dir, "supplier.png")
supplier_icon= PhotoImage(file=img_path3)

supplier_Button = Button(leftFrame,image=supplier_icon, compound=LEFT,text=" Supliers",font=("times new roman", 20, "bold"),anchor="w",command=lambda:show_form(supplier_form))
supplier_Button.pack(fill=X)

img_path4 = os.path.join(script_dir, "product.png")
product_icon= PhotoImage(file=img_path4)

product_Button = Button(leftFrame,image=product_icon, compound=LEFT,text=" Products",font=("times new roman", 20, "bold"),anchor="w",command=lambda:show_form(product_form))
product_Button.pack(fill=X)

img_path5 = os.path.join(script_dir, "categorization.png")
category_icon= PhotoImage(file=img_path5)

category_Button = Button(leftFrame,image=category_icon, compound=LEFT,text=" Category",font=("times new roman", 20, "bold"),anchor="w",command=lambda :show_form(category_form))
category_Button.pack(fill=X)

img_path11 = os.path.join(script_dir, "sales.png")
sales_icon= PhotoImage(file=img_path11)

sales_Button = Button(leftFrame,image=category_icon, compound=LEFT,text=" Sales",font=("times new roman", 20, "bold"),anchor="w")
sales_Button.pack(fill=X)

img_path12 = os.path.join(script_dir, "tax.png")
tax_icon= PhotoImage(file=img_path11)
tax_Button = Button(leftFrame,image=tax_icon, compound=LEFT,text="Tax",font=("times new roman", 20, "bold"),anchor="w",command=lambda:tax_window())
tax_Button.pack(fill=X)

img_path6 = os.path.join(script_dir, "exit.png")
exit_icon= PhotoImage(file=img_path6)

exit_Button = Button(leftFrame,image=exit_icon, compound=LEFT,text=" Exit",font=("times new roman", 20, "bold"),anchor="w")
exit_Button.pack(fill=X)

emp_frame = Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
emp_frame.place(x=400,y=125,width=280,height=170)

img_path7 = os.path.join(script_dir, "staff.png")
total_emp_icon= PhotoImage(file=img_path7)
total_emp_icon_label= Label(emp_frame,image=total_emp_icon,bg="#2C3E50")
total_emp_icon_label.pack()

total_emp_label= Label(emp_frame,text="Total Employees",bg="#2C3E50",fg="white",font=("times new roman", 15, "bold"))
total_emp_label.pack()

total_emp_count_label= Label(emp_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30, "bold"))
total_emp_count_label.pack()


sup_frame = Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
sup_frame.place(x=750,y=125,width=280,height=170)

img_path8 = os.path.join(script_dir, "supplier_frame.png")
total_sup_icon= PhotoImage(file=img_path8)
total_sup_icon_label= Label(sup_frame,image=total_sup_icon,bg="#2C3E50")
total_sup_icon_label.pack()

total_sup_label= Label(sup_frame,text="Total Suppliers",bg="#2C3E50",fg="white",font=("times new roman", 15, "bold"))
total_sup_label.pack()

total_sup_count_label= Label(sup_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30, "bold"))
total_sup_count_label.pack()


pdt_frame = Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
pdt_frame.place(x=400,y=300,width=280,height=170)

img_path9 = os.path.join(script_dir, "products_frame.png")
total_pdt_icon= PhotoImage(file=img_path9)
total_pdt_icon_label= Label(pdt_frame,image=total_pdt_icon,bg="#2C3E50")
total_pdt_icon_label.pack()

total_pdt_label= Label(pdt_frame,text="Total Products",bg="#2C3E50",fg="white",font=("times new roman", 15, "bold"))
total_pdt_label.pack()

total_pdt_count_label= Label(pdt_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30, "bold"))
total_pdt_count_label.pack()


cat_frame = Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
cat_frame.place(x=750,y=300,width=280,height=170)

img_path10 = os.path.join(script_dir, "category.png")
total_cat_icon= PhotoImage(file=img_path10)
total_cat_icon_label= Label(cat_frame,image=total_cat_icon,bg="#2C3E50")
total_cat_icon_label.pack()

total_cat_label= Label(cat_frame,text="Total Categories",bg="#2C3E50",fg="white",font=("times new roman", 15, "bold"))
total_cat_label.pack()

total_cat_count_label= Label(cat_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30, "bold"))
total_cat_count_label.pack()


sale_frame = Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
sale_frame.place(x=575,y=475,width=280,height=170)

img_path12 = os.path.join(script_dir, "growth.png")
total_sale_icon= PhotoImage(file=img_path12)
total_sale_icon_label= Label(sale_frame,image=total_sale_icon,bg="#2C3E50")
total_sale_icon_label.pack()

total_sale_label= Label(sale_frame,text="Total Sales",bg="#2C3E50",fg="white",font=("times new roman", 15, "bold"))
total_sale_label.pack()

total_sale_count_label= Label(sale_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30, "bold"))
total_sale_count_label.pack()

update()
connect_database()
window.mainloop()