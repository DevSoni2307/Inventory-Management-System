# Inventory-Management-System
# Inventory Management System

This project is a desktop-based Inventory Management System built using Python and the `tkinter` library for the graphical user interface (GUI). It connects to a MySQL database to manage employees, suppliers, product categories, and products.

---

## Features

The system is organized into several key modules, all accessible from a central dashboard:

* **Dashboard**: The main application window that displays a summary of key metrics, including the total count of employees, suppliers, categories, and products.
* **Employee Management**: Allows for adding, updating, deleting, and searching for employee records in the database.
* **Supplier Management**: Provides full CRUD (Create, Read, Update, Delete) functionality for managing supplier information.
* **Category Management**: A module to add and delete product categories.
* **Product Management**: Allows for adding, updating, deleting, and searching products, linking them to existing suppliers and categories.

---

## Technology Stack

* **Programming Language**: Python
* **GUI**: `tkinter` (Python's standard GUI package)
* **Database**: MySQL
* **Python Libraries**:
    * `pymysql`: For connecting to the MySQL database.
    * `tkcalendar`: Used for date-entry widgets in the employee form.

---

## Setup and Installation

To run this project on your local machine, follow these steps:

### 1. Prerequisites

* **Python 3.x**
* **MySQL Server**: Ensure you have a MySQL server running (e.g., MySQL Community Server, XAMPP, WAMP).

### 2. Install Required Libraries

You must install the necessary Python libraries. Open your terminal and run:

```bash
pip install pymysql tkcalendar
