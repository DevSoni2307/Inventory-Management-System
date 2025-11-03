# Inventory Management System (Detailed)

This is a comprehensive desktop application for managing inventory, built with Python. It features a multi-window graphical user interface (GUI) using `tkinter` and connects to a MySQL database to persist all data.

The system allows administrators to manage all core aspects of an inventory: employees, suppliers, product categories, and the products themselves.

---

## 1. Core Features

The application is split into five key modules, all launched from a central dashboard.

### 1.1. Dashboard (`dashboard.py`)

This is the main entry point and central hub of the application.
* **Live Statistics**: Displays real-time counts for:
    * Total Employees
    * Total Suppliers
    * Total Products
    * Total Categories
* **Dynamic Clock**: Shows the current date and time, updating every second.
* **Navigation**: Provides buttons to open the individual management modules (Employee, Supplier, Category, Product).
* **Automatic Updates**: The dashboard queries the database every second to keep the summary counts accurate.

### 1.2. Employee Management (`employee.py`)

Provides full CRUD (Create, Read, Update, Delete) functionality for employee records.
* **Data Fields**:
    * Employee ID (Auto-incremented)
    * Name, Email, Contact
    * Gender (Combobox)
    * DOB (Date Entry Calendar)
    * DOJ (Date Entry Calendar)
    * Employment Type, Education, Work Shift (Comboboxes)
    * Address (Text Area)
    * Salary
    * User Type (Combobox: Admin/Employee)
    * Password
* **Functions**:
    * **Add**: Saves a new employee record to the database.
    * **Update**: Modifies an existing employee's details.
    * **Delete**: Removes an employee from the database.
    * **Clear**: Resets all entry fields.

### 1.3. Supplier Management (`supplier.py`)

Manages information for all product suppliers.
* **Data Fields**:
    * Invoice No. (Primary Key)
    * Supplier Name
    * Contact
    * Description (Text Area)
* **Functions**:
    * **Add, Update, Delete, Clear**: Full CRUD operations for suppliers.
    * **Live Data Display**: A `ttk.Treeview` widget lists all suppliers currently in the database.
    * **Search**: Allows searching for a supplier by their name.

### 1.4. Category Management (`category.py`)

Manages the different categories for products.
* **Data Fields**:
    * Category ID (Auto-incremented)
    * Category Name
    * Description (Text Area)
* **Functions**:
    * **Add**: Saves a new product category.
    * **Delete**: Removes a selected category.
    * **Clear**: Resets the entry fields.
    * **Live Data Display**: A `ttk.Treeview` widget shows all existing categories.

### 1.5. Product Management (`products.py`)

The most complex module, tying together categories and suppliers to manage products.
* **Data Fields**:
    * Product ID (Auto-incremented)
    * Category (Combobox, dynamically populated from the `category_data` table)
    * Supplier (Combobox, dynamically populated from the `supplier_data` table)
    * Product Name
    * Price
    * Quantity
    * Status (Combobox: Active/Inactive)
* **Functions**:
    * **Add, Update, Delete, Clear**: Full CRUD operations for products.
    * **Live Data Display**: A `ttk.Treeview` widget displays all product details.
    * **Advanced Search**: Features a search bar where the user can select *which field* to search by (e.g., search by Product ID, Name, Category, or Supplier).

---

## 2. Technology Stack

* **Core Language**: Python 3
* **GUI**: `tkinter` and `tkinter.ttk`
* **Database**: `MySQL`
* **Python Libraries**:
    * `pymysql`: For all MySQL database connections and operations.
    * `tkcalendar`: Used for the user-friendly `DateEntry` calendar widgets in the employee form.

---

## 3. Database Schema

The application automatically creates the database and tables if they do not exist.

**Database Name**: `inventory_system`

**Tables**:

1.  **`employee_data`** (from `employee.py`)
    * `empid` INT PRIMARY KEY AUTO_INCREMENT
    * `name` VARCHAR(100)
    * `email` VARCHAR(100)
    * `gender` VARCHAR(50)
    * `dob` VARCHAR(30)
    * `contact` VARCHAR(30)
    * `employement_type` VARCHAR(50)
    * `education` VARCHAR(50)
    * `work_shift` VARCHAR(50)
    * `address` TEXT
    * `doj` VARCHAR(30)
    * `salary` VARCHAR(50)
    * `usertype` VARCHAR(50)
    * `password` VARCHAR(50)

2.  **`supplier_data`** (inferred from `supplier.py`'s functions)
    * `invoice` VARCHAR(50) PRIMARY KEY (based on `add_supplier` query)
    * `name` VARCHAR(100)
    * `contact` VARCHAR(30)
    * `description` TEXT

3.  **`category_data`** (from `category.py`)
    * `id` INT PRIMARY KEY AUTO_INCREMENT
    * `name` VARCHAR(100)
    * `description` TEXT

4.  **`product_data`** (inferred from `products.py`'s functions)
    * `id` INT PRIMARY KEY AUTO_INCREMENT (based on `add_product` query)
    * `category` VARCHAR(100)
    * `supplier` VARCHAR(100)
    * `name` VARCHAR(100)
    * `price` VARCHAR(50)
    * `quantity` VARCHAR(50)
    * `status` VARCHAR(50)

---

## 4. Setup and Installation

Follow these steps to run the project on your local machine.

### 4.1. Prerequisites

* **Python 3.x**: Ensure Python is installed and added to your system's PATH.
* **MySQL Server**: You must have a running MySQL server instance (e.g., MySQL Community Server, XAMPP, WAMP).

### 4.2. Install Required Libraries

Open your terminal or command prompt and install the necessary Python packages:
```bash
pip install pymysql, tkcalendar, messagebox
