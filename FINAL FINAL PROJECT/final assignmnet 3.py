import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import pickle
import os
import random
from ENUMS import ServiceType, EventType
from CLASSES import Person, Employee, Client, Service, Catering, Supplier, Guest, Event, Venue


class EventManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the Tk parent class
        self.title("The Best Events Company Management System")  # Set the window title
        self.geometry('600x450')  # Set the default size of the window

        # Dictionaries to store data about clients, employees, suppliers, and guests
        self.clients = {}
        self.employees = {}
        self.suppliers = {}
        self.supplier_id_counter = 1  # Start supplier ID counter
        self.guests = {}
        self.guest_id_counter = 1
        self.events = {}
        self.event_id_counter = 1
        self.venues = {}
        self.venue_id_counter = 1

        # Setup the initial UI and load any post-initialization configurations
        self.setup_ui()
        self.post_init()



    def post_init(self):
        # Load existing data from files for each category if available
        self.clients = self.load_data('../final assignmnet /clients.pkl')  # Load client data
        self.client_id_counter = max(self.clients.keys(), default=0) + 1 # Update the ID counter
        self.client_id_counter = len(self.clients) + 1 # Ensure unique IDs for new clients

        self.employees = self.load_data('../final assignmnet /employees.pkl')  # Load employee data
        self.employee_id_counter = max(self.employees.keys(), default=0) + 1  # Update the ID counter
        self.employee_id_counter = len(self.employees) + 1

        self.suppliers = self.load_data('../final assignmnet /suppliers.pkl')
        numeric_keys = [k for k in self.suppliers.keys() if isinstance(k, str) and k.isdigit()]
        self.supplier_id_counter = max(numeric_keys, default=0) + 1

        self.guests = self.load_data('../final assignmnet /guests.pkl')  # Load guest data
        self.guest_id_counter = max(map(int, self.guests.keys()), default=0) + 1
        self.guest_id_counter = len(self.guests) + 1

        self.venues = self.load_data('../final assignmnet /venues.pkl')

        # If venues dictionary is not empty, find the maximum key, convert it to int, add 1, and set it as the next venue_id_counter
        if self.venues:
            self.venue_id_counter = max(int(venue_id) for venue_id in self.venues.keys()) + 1
        else:
            # If there are no venues loaded, start the counter at 1
            self.venue_id_counter = 1

        self.events = self.load_data('../final assignmnet /events.pkl')  # Load event data
        self.event_id_counter = max((int(key) for key in self.events.keys()), default=0) + 1  # Update the ID counter
        self.event_id_counter = len(self.events) + 1

    def load_data(self, filename):
        # Load data from a pickle file if it exists, otherwise return an empty dictionary
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_data(self, filename, data):
        # Save the provided data object to a file using pickle
        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def setup_ui(self):
        # Main frame for the application content
        self.main_frame = ttk.Frame(self, padding=(10, 10))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame for the welcome message
        welcome_frame = ttk.Frame(self.main_frame, padding=(20, 20))
        welcome_frame.pack(fill=tk.BOTH, expand=True)

        # Welcome label setup
        welcome_message = "Welcome to The Best Events Company Management System"
        welcome_label = ttk.Label(welcome_frame, text=welcome_message, font=('Arial', 16, 'bold'),
                                  background='#f0f0f0',  # Consistent background color
                                  wraplength=500)  # Wrap text to fit into the specified width
        welcome_label.pack(pady=(20, 10), padx=10, fill=tk.X)  # Add padding and fill the X-axis

        # Frame for the proceed button
        button_frame = ttk.Frame(self.main_frame, padding=(10, 10))
        button_frame.pack(fill=tk.X, expand=True)

        # Button to proceed to the login screen
        proceed_button = ttk.Button(button_frame, text="Proceed to Login", command=self.login_ui,
                                    style='TButton')
        proceed_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Place the button on the right side

        # Style configuration for the button with hover effect
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), borderwidth=1)
        style.map('TButton', foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'), ('active', 'white')])

    def login_ui(self):
        # Destroy the main/welcome frame and setup the login frame
        self.main_frame.destroy()
        self.login_frame = ttk.Frame(self, padding=(10, 10), style='TFrame')
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Label for login prompt
        ttk.Label(self.login_frame, text="Login as:", font=('Helvetica', 12)).pack(pady=(20, 10))

        # Options for login types
        login_options = ["Employee", "Guest", "Client", "Supplier", "Event", "Venue"]
        self.login_type = tk.StringVar(value="Employee")
        for option in login_options:
            # Radio button for each login type
            ttk.Radiobutton(self.login_frame, text=option, variable=self.login_type, value=option,
                            style='TRadiobutton').pack(fill=tk.X)

        # Button to proceed based on selected login type
        ttk.Button(self.login_frame, text="Proceed", command=self.proceed_login).pack(pady=20)

    def proceed_login(self):
        # Determine the type of user and display the corresponding UI
        login_type = self.login_type.get()
        self.login_frame.destroy()  # Destroy the current login frame
        if login_type == "Employee":
            self.employee_ui()
        elif login_type == "Guest":
            self.guests_ui()
        elif login_type == "Client":
            self.client_ui()
        elif login_type == "Supplier":
            self.supplier_ui()
        elif login_type == "Event":
            self.event_ui()
        elif login_type == "Venue":
            self.venue_ui()

    def employee_ui(self):
        # Clear any existing widgets from the application's main window
        self.clear_frame()
        # Create a new frame for employee management and add it to the main window
        self.employee_frame = ttk.Frame(self)
        self.employee_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a header label to the employee management frame
        header_label = ttk.Label(self.employee_frame, text="Employee Management", font=("Arial", 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=(10, 20))

        # Add a button to go back to the main menu
        ttk.Button(self.employee_frame, text="Back to Main Menu", command=self.login_ui).pack(pady=20)
        # Add a button to trigger the UI for adding a new employee
        ttk.Button(self.employee_frame, text="Add New Employee", command=self.add_employee_ui).pack(fill=tk.X)

        # Call function to display the list of employees
        self.employee_list_ui()

    def search_employee_ui(self):
        # Create a frame for searching employees and add it to the employee frame
        search_frame = ttk.Frame(self.employee_frame)
        search_frame.pack(fill=tk.X, padx=10)
        # Label for the search input field
        ttk.Label(search_frame, text="Search by ID:").pack(side=tk.LEFT)
        # Entry widget for entering the search term (employee ID)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, padx=10)
        # Button to initiate search; uses lambda to pass search input to the find_employee function
        ttk.Button(search_frame, text="Search", command=lambda: self.find_employee(search_entry.get())).pack(
            side=tk.LEFT)

    def find_employee(self, emp_id):
        # Attempt to convert input to an integer, catch ValueError if input is not a valid integer
        try:
            emp_id = int(emp_id)
            # Check if employee ID exists in the employee dictionary
            if emp_id in self.employees:
                # If found, call the function to edit the employee's details
                self.edit_employee_ui(emp_id)
            else:
                # If not found, display a message box with "Not Found"
                messagebox.showinfo("Not Found", "Employee ID not found.")
        except ValueError:
            # Display an error message if input is not a valid integer
            messagebox.showerror("Error", "Invalid ID. Please enter a numeric ID.")

    def display_employee_details(self, employee):
        # Assuming you want to display details below or in another widget
        detail_frame = ttk.Frame(self.employee_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(detail_frame, text=f"Name: {employee.name}").pack()
        # Job Title Combobox
        job_title_label = ttk.Label(detail_frame, text="Job Title:")
        job_title_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        job_titles = ["Manager", "Assistant", "Clerk", "Supervisor"]  # Example job titles
        job_title_combobox = ttk.Combobox(detail_frame, values=job_titles)
        job_title_combobox.set(employee.job_title)  # Set to current job title
        job_title_combobox.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Department Combobox
        department_label = ttk.Label(detail_frame, text="Department:")
        department_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        departments = ["HR", "Marketing", "Finance", "Sales"]  # Example departments
        department_combobox = ttk.Combobox(detail_frame, values=departments)
        department_combobox.set(employee.department)  # Set to current department
        department_combobox.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(detail_frame, text=f"Salary: ${employee.salary}").pack()

    def setup_comboboxes(self, detail_frame, employee):
        departments = ["HR", "Marketing", "Finance", "Sales"]
        department_var = tk.StringVar(value=employee.department)  # Preset with current department
        department_combobox = ttk.Combobox(detail_frame, textvariable=department_var, values=departments,
                                           state='readonly')
        department_combobox.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.update_idletasks()  # Update UI immediately

    def employee_list_ui(self):
        # If an employee list frame already exists, destroy it to refresh the content
        if hasattr(self, 'employee_list_frame'):
            self.employee_list_frame.destroy()

        # Create a new frame for displaying the list of employees and add it to the employee frame
        self.employee_list_frame = ttk.Frame(self.employee_frame)
        self.employee_list_frame.pack(fill=tk.BOTH, expand=True)

        # Define the columns for the Treeview widget that will display the employee list
        columns = ("ID", "Name", "Department", "Job Title", "Salary")
        self.employee_table = ttk.Treeview(self.employee_list_frame, columns=columns, show="headings")
        # Configure each column's heading and width
        for col in columns:
            self.employee_table.heading(col, text=col)
            self.employee_table.column(col, width=100)
        # Pack the Treeview widget into the employee list frame
        self.employee_table.pack(fill=tk.BOTH, expand=True, pady=10)
        # Populate the employee table with data
        self.populate_employee_table()

        # Add buttons for modifying and deleting selected employees, and for initiating a search
        ttk.Button(self.employee_list_frame, text="Modify Selected", command=self.modify_selected_employee).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.employee_list_frame, text="Delete Selected", command=self.delete_selected_employee).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.employee_list_frame, text="Search Selected", command=self.search_employee_ui).pack(side=tk.LEFT,
                                                                                                           padx=10)

    def populate_employee_table(self):
        # Clear existing entries in the employee table
        for i in self.employee_table.get_children():
            self.employee_table.delete(i)
        # Insert new entries into the employee table
        for emp_id, emp in self.employees.items():
            self.employee_table.insert('', 'end', iid=emp_id,
                                       values=(emp.ID, emp.name, emp.department, emp.job_title, emp.salary))

    def add_employee_ui(self):
        # Clear any existing UI elements before displaying the form
        self.clear_frame()
        # Create a frame for the add employee form
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        # Entry widgets for entering new employee details
        name_entry = ttk.Entry(form_frame)
        department_entry = ttk.Entry(form_frame)
        job_title_entry = ttk.Entry(form_frame)
        salary_entry = ttk.Entry(form_frame)
        entries = (name_entry, department_entry, job_title_entry, salary_entry)
        labels = ("Name:", "Department:", "Job Title:", "Salary:")

        # Create and grid labels and entry widgets in the form
        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0)
            entries[idx].grid(row=idx, column=1)

        # Button to save the new employee data
        ttk.Button(form_frame, text="Save Employee", command=lambda: self.save_employee(
            name_entry.get(), department_entry.get(), job_title_entry.get(), salary_entry.get()
        )).grid(row=4, column=1, pady=10)
        # Button to cancel the operation and return to the employee UI
        ttk.Button(form_frame, text="Cancel", command=self.employee_ui).grid(row=4, column=0)

    def save_employee(self, name, department, job_title, salary):
        # Ensure all fields are filled
        if not all([name, department, job_title, salary]):
            messagebox.showerror("Error", "All fields are required")
            return

        # Create a new employee object and add it to the employees dictionary
        new_employee = Employee(self.employee_id_counter, name, "", "", department, job_title, salary)
        self.employees[self.employee_id_counter] = new_employee
        # Increment the employee ID counter for the next addition
        self.employee_id_counter += 1
        # Save the updated employees data to a file
        self.save_data('../final assignmnet /employees.pkl', self.employees)
        # Show a success message and return to the main employee UI
        messagebox.showinfo("Success", "Employee added successfully")
        self.employee_ui()

    def modify_selected_employee(self):
        # Get the ID of the currently selected employee from the employee table
        selected_item = self.employee_table.focus()
        if selected_item:
            # If an item is selected, open the edit employee UI
            self.edit_employee_ui(int(selected_item))

    def delete_selected_employee(self):
        # Confirm with the user before deleting an employee
        selected_item = self.employee_table.focus()
        if selected_item:
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
            if response:
                # If confirmed, delete the employee from the dictionary
                del self.employees[int(selected_item)]
                # Save the updated employees data to a file
                self.save_data('../final assignmnet /employees.pkl', self.employees)
                # Refresh the employee list UI
                self.employee_list_ui()

    def edit_employee_ui(self, emp_id):
        employee = self.employees[emp_id]
        self.clear_frame()
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, employee.name)
        department_entry = ttk.Entry(form_frame)
        department_entry.insert(0, employee.department)
        job_title_entry = ttk.Entry(form_frame)
        job_title_entry.insert(0, employee.job_title)
        salary_entry = ttk.Entry(form_frame)
        salary_entry.insert(0, employee.salary)
        entries = (name_entry, department_entry, job_title_entry, salary_entry)

        labels = ("Name:", "Department:", "Job Title:", "Salary:")
        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0)
            entries[idx].grid(row=idx, column=1)

        ttk.Button(form_frame, text="Save Changes", command=lambda: self.update_employee(
            emp_id, name_entry.get(), department_entry.get(), job_title_entry.get(), salary_entry.get()
        )).grid(row=4, column=1, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.employee_ui).grid(row=4, column=0)

    def update_employee(self, emp_id, name, department, job_title, salary):
        if not all([name, department, job_title, salary]):
            messagebox.showerror("Error", "All fields are required")
            return

        employee = self.employees[emp_id]
        employee.modify(name, department, job_title, salary)
        self.save_data('../final assignmnet /employees.pkl', self.employees)
        messagebox.showinfo("Success", "Employee updated successfully")
        self.employee_ui()

    def clear_frame(self):
        # Destroy all widgets that are children of the current Tkinter window
        for widget in self.winfo_children():
            widget.destroy()

#--------------------------------------------------------------------------

    def client_ui(self):
        # Clear any existing widgets from the application's main window
        self.clear_frame()

        # Create a new frame for client management and add it to the main window
        self.client_frame = ttk.Frame(self)
        self.client_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a header label to the client management frame
        header_label = ttk.Label(self.client_frame, text="Client Management", font=("Arial", 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=(10, 20))

        # Add a button to go back to the main menu
        ttk.Button(self.client_frame, text="Back to Main Menu", command=self.login_ui).pack(pady=20)

        # Add a button to trigger the UI for adding a new client
        ttk.Button(self.client_frame, text="Add New Client", command=self.add_client_ui).pack(fill=tk.X)

        # Call function to display the list of clients
        self.client_list_ui()

    def add_client_ui(self):
        self.clear_frame()
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        # Entry widgets for entering new client details
        name_entry = ttk.Entry(form_frame)
        address_entry = ttk.Entry(form_frame)
        contact_details_entry = ttk.Entry(form_frame)
        budget_entry = ttk.Entry(form_frame)
        event_type_combobox = ttk.Combobox(form_frame, values=[e.name for e in EventType], state="readonly")

        entries = [name_entry, address_entry, contact_details_entry, budget_entry, event_type_combobox]
        labels = ["Name:", "Address:", "Contact Details:", "Budget:", "Event Type:"]

        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0)
            entries[idx].grid(row=idx, column=1)

        ttk.Button(form_frame, text="Save Client", command=lambda: self.save_client(
            name_entry.get(), address_entry.get(), contact_details_entry.get(), budget_entry.get(),
            EventType[event_type_combobox.get()]
        )).grid(row=5, column=1, pady=10)

        ttk.Button(form_frame, text="Cancel", command=self.client_ui).grid(row=5, column=0)

    def save_client(self, name, address, contact_details, budget, event_type):
        if not all([name, address, contact_details, budget]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            new_client = Client(self.client_id_counter, name, address, contact_details, float(budget))
            new_client.add_event(event_type)  # Assuming event_type is properly received
            self.clients[self.client_id_counter] = new_client
            self.client_id_counter += 1
            self.save_data('../final assignmnet /clients.pkl', self.clients)
            messagebox.showinfo("Success", "Client added successfully")
            self.client_ui()
        except ValueError:
            messagebox.showerror("Error", "Invalid budget. Please enter a numeric value.")

    def client_list_ui(self):
        # If a client list frame already exists, destroy it to refresh the content
        if hasattr(self, 'client_list_frame'):
            self.client_list_frame.destroy()

        # Create a new frame for displaying the list of clients and add it to the client frame
        self.client_list_frame = ttk.Frame(self.client_frame)
        self.client_list_frame.pack(fill=tk.BOTH, expand=True)

        # Define the columns for the Treeview widget that will display the client list
        columns = ("ID", "Name", "Address", "Contact Details", "Budget", "Events")
        self.client_table = ttk.Treeview(self.client_list_frame, columns=columns, show="headings")
        # Configure each column's heading and width
        for col in columns:
            self.client_table.heading(col, text=col)
            self.client_table.column(col, width=100)
        # Pack the Treeview widget into the client list frame
        self.client_table.pack(fill=tk.BOTH, expand=True, pady=10)
        # Populate the client table with data
        self.populate_client_table()

        # Add buttons for modifying and deleting selected clients
        ttk.Button(self.client_list_frame, text="Modify Selected", command=self.modify_selected_client).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.client_list_frame, text="Delete Selected", command=self.delete_selected_client).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.client_list_frame, text="Search Selected", command=self.search_client_ui).pack(side=tk.LEFT, padx=10)


    def search_client_ui(self):
        # This method will be triggered by the 'Search Selected' button
        client_id = simpledialog.askstring("Search Client", "Enter Client ID:")
        if client_id:
            self.find_client(client_id)
        else:
            messagebox.showinfo("Search", "No ID entered.")

    def populate_client_table(self):
        for i in self.client_table.get_children():
            self.client_table.delete(i)
        for client_id, client in self.clients.items():
            event_types = ", ".join([event.name for event in client.events])
            self.client_table.insert('', 'end', iid=client_id,
                                     values=(client.ID, client.name, client.address, client.contact, client.budget,
                                             event_types))

    def modify_selected_client(self):
        selected_item = self.client_table.focus()
        if selected_item:
            self.edit_client_ui(int(selected_item))


    def delete_selected_client(self):
        selected_item = self.client_table.focus()
        if selected_item:
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this client?")
            if response:
                del self.clients[int(selected_item)]
                self.save_data('../final assignmnet /clients.pkl', self.clients)
                self.client_list_ui()

    def update_client(self, client_id, name, address, contact_details, budget):
        if not all([name, address, contact_details, budget]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            client = self.clients[client_id]
            client.name = name
            client.address = address
            client.contact = contact_details
            client.budget = float(budget)  # Ensure conversion to float
            self.save_data('../final assignmnet /clients.pkl', self.clients)
            messagebox.showinfo("Success", "Client updated successfully")
            self.client_ui()  # Refresh the client UI
        except ValueError:
            messagebox.showerror("Error", "Invalid input for budget. Please enter a numeric value.")

    def edit_client_ui(self, client_id):
        client = self.clients[client_id]
        self.clear_frame()

        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, client.name)
        address_entry = ttk.Entry(form_frame)
        address_entry.insert(0, client.address)
        contact_details_entry = ttk.Entry(form_frame)
        contact_details_entry.insert(0, client.contact)
        budget_entry = ttk.Entry(form_frame)
        budget_entry.insert(0, str(client.budget))

        entries = (name_entry, address_entry, contact_details_entry, budget_entry)
        labels = ("Name:", "Address:", "Contact Details:", "Budget:")

        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0)
            entries[idx].grid(row=idx, column=1)

        ttk.Button(form_frame, text="Save Changes", command=lambda: self.update_client(
            client_id, name_entry.get(), address_entry.get(), contact_details_entry.get(), budget_entry.get()
        )).grid(row=4, column=1, pady=10)

        ttk.Button(form_frame, text="Cancel", command=self.client_ui).grid(row=4, column=0)

    def find_client(self, client_id):
        try:
            client_id = int(client_id)
            if client_id in self.clients:
                self.edit_client_ui(client_id)
            else:
                messagebox.showinfo("Not Found", "Client ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid ID. Please enter a numeric ID.")
#----------------------------------------------------------------------------------
    def supplier_ui(self):
        # Check and reinitialize if necessary
        if hasattr(self, 'supplier_frame') and self.supplier_frame.winfo_exists():
            self.clear_frame()
        else:
            self.supplier_frame = ttk.Frame(self)
            self.supplier_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        # Add a header label to the supplier management frame
        header_label = ttk.Label(self.supplier_frame, text="Supplier Management", font=("Arial", 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=(10, 20))

        ttk.Button(self.supplier_frame, text="Add New Supplier", command=self.add_supplier_ui).pack(fill=tk.X)
        ttk.Button(self.supplier_frame, text="Back to Main Menu", command=self.login_ui).pack(pady=20)

        self.supplier_list_ui()

    def clear_frame(self):
        for widget in self.supplier_frame.winfo_children():
            widget.destroy()

    def add_supplier_ui(self):
        self.clear_frame()  # Clear only the child widgets inside supplier_frame

        # Reinitialize supplier_frame if it has been destroyed or does not exist
        if not hasattr(self, 'supplier_frame') or not self.supplier_frame.winfo_exists():
            self.supplier_frame = ttk.Frame(self)
            self.supplier_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        print(f"Supplier Frame Exists: {'Yes' if self.supplier_frame.winfo_exists() else 'No'}")

        # Create a new frame inside supplier_frame to hold form widgets
        form_frame = ttk.Frame(self.supplier_frame)
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


        # Setup entry widgets
        name_entry = ttk.Entry(form_frame)
        address_entry = ttk.Entry(form_frame)
        contact_details_entry = ttk.Entry(form_frame)
        max_guests_entry = ttk.Entry(form_frame)
        min_guests_entry = ttk.Entry(form_frame)
        event_type_combobox = ttk.Combobox(form_frame, values=[e.name for e in EventType], state="readonly")

        entries = [name_entry, address_entry, contact_details_entry, max_guests_entry, min_guests_entry,
                   event_type_combobox]
        labels = ["Name:", "Address:", "Contact Details:", "Max Guests:", "Min Guests:", "Event Type:"]

        # Place labels and entries in the grid
        for idx, label in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=idx, column=0, sticky="e")
            entries[idx].grid(row=idx, column=1, sticky="w")

        # Buttons for saving or canceling
        ttk.Button(form_frame, text="Save Supplier", command=lambda: self.save_supplier(
            name_entry.get(), address_entry.get(), contact_details_entry.get(),
            max_guests_entry.get(), min_guests_entry.get(), event_type_combobox.get()
        )).grid(row=7, column=1, pady=10, sticky="e")

        ttk.Button(form_frame, text="Cancel", command=self.supplier_ui).grid(row=7, column=0, sticky="w")

    def save_supplier(self, name, address, contact_details, max_guests, min_guests, event_type_str):
        try:
            max_guests = int(max_guests)
            min_guests = int(min_guests)
        except ValueError:
            messagebox.showerror("Error", "Max Guests and Min Guests must be numbers")
            return

        if not all([name, address, contact_details, max_guests, min_guests, event_type_str]):
            messagebox.showerror("Error", "All fields are required")
            return

        # Validate the event type
        try:
            event_type = EventType[event_type_str]
        except KeyError:
            messagebox.showerror("Error", "Invalid Event Type")
            return

        # Create or update the Supplier object
        supplier_id = self.get_next_supplier_id()  # Assuming a method to generate unique IDs or handle existing ones
        new_supplier = Supplier(supplier_id, name, address, contact_details, [event_type], min_guests, max_guests)

        # Save or update the supplier in a collection
        self.suppliers[supplier_id] = new_supplier  # Assuming self.suppliers is a dictionary

        # Save to file or database if needed
        # self.save_to_database(new_supplier)  # This is an example placeholder

        # Notify user of success
        messagebox.showinfo("Success", "Supplier saved successfully")

        # Refresh the UI
        self.populate_supplier_table()  # Refresh the supplier list UI

    def get_next_supplier_id(self):
        # Print keys for debugging purposes
        print(self.suppliers.keys())

        # Conversion to integers ensuring all keys are numeric
        int_keys = [int(k) for k in self.suppliers.keys() if isinstance(k, int) or (isinstance(k, str) and k.isdigit())]

        # Find the maximum integer key and add 1 to generate the next ID
        next_id = max(int_keys, default=0) + 1
        return next_id

    def supplier_list_ui(self):

        if hasattr(self, 'supplier_list_frame'):
            self.supplier_list_frame.destroy()

        # Create a new frame for displaying the list of suppliers and add it to the supplier frame
        self.supplier_list_frame = ttk.Frame(self.supplier_frame)
        self.supplier_list_frame.pack(fill=tk.BOTH, expand=True)

        # Define the columns for the Treeview widget that will display the supplier list
        columns = ("ID", "Name", "Event Type", "Address", "Contact Details", "Min Guests", "Max Guests")
        self.supplier_table = ttk.Treeview(self.supplier_list_frame, columns=columns, show="headings")

        # Configure each column's heading and width
        for col in columns:
            self.supplier_table.heading(col, text=col)
            self.supplier_table.column(col, width=100)

        # Pack the Treeview widget into the supplier list frame
        self.supplier_table.pack(fill=tk.BOTH, expand=True, pady=10)

        # Populate the supplier table with data
        self.populate_supplier_table()

        # Add buttons for modifying and deleting selected suppliers
        ttk.Button(self.supplier_list_frame, text="Modify Selected", command=self.modify_selected_supplier).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.supplier_list_frame, text="Delete Selected", command=self.delete_selected_supplier).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(self.supplier_list_frame, text="Search Selected", command=self.search_supplier_ui).pack(side=tk.LEFT,
                                                                                                           padx=10)

    # Example of loading data with checks or defaults
    def load_suppliers(self):
        # assuming data is a dictionary loaded from a file
        for data in loaded_data:
            supplier = Supplier(
                supplier_id=data.get('supplier_id'),
                name=data.get('name', 'Unknown Name'),  # Default if name is missing
                address=data.get('address', 'No address provided'),  # Default if address is missing
                contact_details=data.get('contact_details', 'No contact details'),
                # Default if contact details are missing
                event_type=data.get('event_type', None),  # Default if event type is missing
                min_guests=data.get('min_guests', 0),  # Default if min guests is missing
                max_guests=data.get('max_guests', 0)  # Default if max guests is missing
            )
            self.suppliers[supplier.supplier_id] = supplier

    def create_widgets(self):
        # Assuming you have a frame or some container for the Treeview
        self.supplier_table_frame = ttk.Frame(self.master)
        self.supplier_table_frame.pack(fill='both', expand=True)

        # Create the Treeview widget
        self.supplier_table = ttk.Treeview(self.supplier_table_frame)

        # Define the columns
        self.supplier_table['columns'] = ('Supplier ID', 'Supplier Name', 'Contact')

        # Format our columns
        self.supplier_table.column("#0", width=0, stretch=tk.NO)
        self.supplier_table.column("Supplier ID", anchor=tk.W, width=120)
        self.supplier_table.column("Supplier Name", anchor=tk.W, width=120)
        self.supplier_table.column("Contact", anchor=tk.CENTER, width=120)

        # Create Headings
        self.supplier_table.heading("#0", text="", anchor=tk.W)
        self.supplier_table.heading("Supplier ID", text="ID", anchor=tk.W)
        self.supplier_table.heading("Supplier Name", text="Name", anchor=tk.W)
        self.supplier_table.heading("Contact", text="Contact", anchor=tk.CENTER)

        # Add the Treeview to the frame
        self.supplier_table.pack(side="top", fill="both", expand=True)

        # Now that the Treeview is created, you can populate it
        self.populate_supplier_table()

    def populate_supplier_table(self):
        for i in self.supplier_table.get_children():
            self.supplier_table.delete(i)

        for supplier_id, supplier in self.suppliers.items():
            # Ensure all necessary attributes are present and correct type
            if not all(hasattr(supplier, attr) for attr in ['min_guests', 'max_guests', 'event_type']):
                print(f"Error: Supplier {supplier_id} is missing required attributes.")
                continue

            print(
                f"Supplier {supplier_id} loaded with event_type={supplier.event_type}, min_guests={supplier.min_guests}, max_guests={supplier.max_guests}")
            # Assuming event_type is properly initialized
            event_type_name = ', '.join([et.name for et in supplier.event_type]) if isinstance(supplier.event_type,
                                                                                               list) else supplier.event_type.name
            self.supplier_table.insert('', 'end', iid=supplier_id,
                                       values=(supplier_id, supplier.name, event_type_name,
                                               supplier.address, supplier.contact_details, supplier.min_guests,
                                               supplier.max_guests))

    def modify_selected_supplier(self):
        selected_item = self.supplier_table.focus()  # Get the selected supplier
        if selected_item:
            self.edit_supplier_ui(int(selected_item))


    def delete_selected_supplier(self):
        selected_item = self.supplier_table.focus()  # Get the selected supplier
        if selected_item:
            confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this supplier?")
            if confirmation:
                del self.suppliers[int(selected_item)]  # Remove the selected supplier
                self.save_data('../final assignmnet /suppliers.pkl', self.suppliers)  # Save the updated supplier list
                self.supplier_list_ui()  # Refresh the supplier list UI

    def search_supplier_ui(self):
        search_id = simpledialog.askinteger("Search Supplier", "Enter Supplier ID:")
        if search_id in self.suppliers:
            self.edit_supplier_ui(search_id)  # Edit the supplier if found
        else:
            messagebox.showinfo("Search Result", "Supplier with ID {} not found.".format(search_id))

    def update_supplier(self, supplier_id, name, address, contact_details, event_type_str, min_guests, max_guests):
        try:
            # Convert min and max guests to integers
            min_guests = int(min_guests)
            max_guests = int(max_guests)
        except ValueError:
            messagebox.showerror("Error", "Min and Max Guests must be valid numbers")
            return

        try:
            # Attempt to convert event type string to EventType
            event_type = EventType[event_type_str]
        except KeyError:
            messagebox.showerror("Error", "Invalid service or event type")
            return

        if not all([name, address, contact_details, event_type_str, min_guests, max_guests]):
            messagebox.showerror("Error", "All fields are required")
            return

        # Update the supplier details
        supplier = self.suppliers[supplier_id]
        supplier.name = name
        supplier.address = address
        supplier.contact_details = contact_details
        supplier.event_type = event_type
        supplier.min_guests = min_guests
        supplier.max_guests = max_guests

        # Optionally, save to a file or database
        messagebox.showinfo("Success", "Supplier updated successfully")
        self.supplier_list_ui()  # Refresh UI

    # Ensure you bind ComboBox selection properly
    def save_changes(self):
        # Extract data from the form, including the combobox
        self.update_supplier(
            supplier_id,
            name_entry.get(),
            address_entry.get(),
            contact_details_entry.get(),
            event_type_combobox.get(),  # Ensure this gets the selected value
            min_guests_entry.get(),
            max_guests_entry.get()
        )

    def edit_supplier_ui(self, supplier_id):
        supplier = self.suppliers[supplier_id]  # Get the supplier object

        self.clear_frame()
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        # Assuming EventType is an enum or list of event types
        event_type_combobox = ttk.Combobox(form_frame, values=[e.name for e in EventType], state="readonly")
        event_type_combobox.set(supplier.event_type)  # Assuming supplier.event_type is the correct format

        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, supplier.name)
        address_entry = ttk.Entry(form_frame)
        address_entry.insert(0, supplier.address)
        contact_details_entry = ttk.Entry(form_frame)
        contact_details_entry.insert(0, supplier.contact_details)
        min_guests_entry = ttk.Entry(form_frame)
        min_guests_entry.insert(0, str(supplier.min_guests))
        max_guests_entry = ttk.Entry(form_frame)
        max_guests_entry.insert(0, str(supplier.max_guests))

        entries = (
        name_entry, event_type_combobox, address_entry, contact_details_entry, min_guests_entry, max_guests_entry)
        labels = ("Name", "Event Type", "Address", "Contact Details", "Min Guests", "Max Guests")

        for idx, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=idx, column=0, sticky="e")
            entries[idx].grid(row=idx, column=1, sticky="w")

        ttk.Button(form_frame, text="Save Changes", command=lambda: self.update_supplier(
            supplier_id, name_entry.get(), address_entry.get(),
            contact_details_entry.get(), event_type_combobox.get(),
            int(min_guests_entry.get()), int(max_guests_entry.get())
        )).grid(row=6, column=1, pady=10, sticky="w")

        ttk.Button(form_frame, text="Cancel", command=self.supplier_list_ui).grid(row=6, column=0, sticky="w")

    def find_supplier(self, supplier_id):
        try:
            supplier_id = int(supplier_id)
            if supplier_id in self.suppliers:
                self.edit_supplier_ui(supplier_id)
            else:
                messagebox.showinfo("Not Found", "Supplier ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid ID. Please enter a numeric ID.")


    #----------------------------------

    def guests_ui(self):
        self.clear_frame()
        self.guest_frame = ttk.Frame(self)
        self.guest_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Guest Sign-Up Section
        ttk.Label(self.guest_frame, text="Name:").grid(row=0, column=0)
        name_entry = ttk.Entry(self.guest_frame)
        name_entry.grid(row=0, column=1)

        ttk.Label(self.guest_frame, text="Email:").grid(row=1, column=0)
        email_entry = ttk.Entry(self.guest_frame)
        email_entry.grid(row=1, column=1)

        ttk.Label(self.guest_frame, text="Phone Number:").grid(row=2, column=0)
        phone_number_entry = ttk.Entry(self.guest_frame)
        phone_number_entry.grid(row=2, column=1)

        ttk.Label(self.guest_frame, text="Total Cost:").grid(row=3, column=0)
        total_cost_entry = ttk.Entry(self.guest_frame)
        total_cost_entry.grid(row=3, column=1)


        # Hidden till sign up is clicked
        ttk.Button(self.guest_frame, text="Proceed to Events", command=lambda: self.calculate_guest_ui(
            name_entry.get(), email_entry.get(), phone_number_entry.get(), total_cost_entry.get())).grid(row=4,
                                                                                                         column=0)

        ttk.Button(self.guest_frame, text="Back to Main Menu", command=self.login_ui).grid(row=4, column=0)
        ttk.Button(self.guest_frame, text="Delete Selected", command=self.delete_selected_guest).grid(row=6, column=0,
                                                                                                      pady=10)

        # Button to modify a guest's details
        ttk.Button(self.guest_frame, text="Modify Selected", command=self.modify_selected_guest).grid(row=6, column=1,
                                                                                                      pady=10)

        # Search functionality (with entry and button)
        ttk.Label(self.guest_frame, text="Search by ID:").grid(row=7, column=0)
        search_entry = ttk.Entry(self.guest_frame)
        search_entry.grid(row=7, column=1, sticky='we')

        ttk.Button(self.guest_frame, text="Search", command=lambda: self.search_guest_by_id(search_entry.get())).grid(
            row=8, column=1, pady=10)


        # Update the 'Save' button command to include the total cost entry
        ttk.Button(
            self.guest_frame, text="Save",
            command=lambda: self.add_guests_ui(
                name_entry.get(), email_entry.get(), phone_number_entry.get(), total_cost_entry.get()
            )
        ).grid(row=4, column=1, pady=10)

        # This part seems correct, but ensure the widths are set to accommodate the data.
        self.guest_list = ttk.Treeview(self.guest_frame, columns=("Name", "Email", "Phone Number", "Total Cost"))
        self.guest_list.heading("#0", text="ID")
        self.guest_list.column("#0", width=50)

        # Configure the columns.
        for col in ("Name", "Email", "Phone Number", "Total Cost"):
            self.guest_list.heading(col, text=col)
            self.guest_list.column(col, width=120)  # Adjust width as needed

        self.guest_list.grid(row=5, columnspan=2, sticky='nsew')

        # Populate the Treeview with guest data
        self.populate_guest_list()

        # At the end of guests_ui method after the Treeview is created.
        self.guest_list.bind("<<TreeviewSelect>>", self.on_guest_select)

    def populate_guest_list(self):
        # Clear the current view
        for item in self.guest_list.get_children():
            self.guest_list.delete(item)

        # Populate the Treeview with updated guest data
        for guest_id, guest_info in self.guests.items():
            # Provide a default total cost if it doesn't exist
            total_cost = guest_info.get("Total Cost", "0")  # Default to "0" if not present
            self.guest_list.insert("", 'end', iid=guest_id, text=guest_id, values=(
                guest_info["Name"],
                guest_info["Email"],
                guest_info["Phone Number"],
                f"${total_cost}"  # Display the total cost
            ))

    def delete_selected_guest(self):
        selected_item = self.guest_list.selection()
        if selected_item:  # Check if something is selected
            selected_item = selected_item[0]
            # Ask for confirmation before deleting
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected guest?")
            if response:  # If the user clicks 'Yes', proceed with deletion
                self.guest_list.delete(selected_item)
                del self.guests[selected_item]  # Remove from your data structure
                self.save_data('../final assignmnet /guests.pkl', self.guests)  # Save the updated data
        else:
            messagebox.showerror("Error", "No guest selected for deletion.")

    def add_guests_ui(self, name, email, phone_number, total_cost):
        guest_id = str(self.guest_id_counter)
        self.guests[guest_id] = {
            "Name": name,
            "Email": email,
            "Phone Number": phone_number,
            "Total Cost": total_cost  # Include total cost in guest info
        }
        self.guest_id_counter += 1


        # Save the updated guests dictionary to a .pkl file
        self.save_data('../final assignmnet /guests.pkl', self.guests)

        self.populate_guest_list()

        # Display success message to the user
        messagebox.showinfo("Success", f"{name} has been registered successfully!")

    def search_guest_by_id(self, guest_id):
        try:
            guest_id_str = str(guest_id)  # Convert to string if your IDs are strings
            guest_info = self.guests.get(guest_id_str)

            if guest_info:
                # Select and focus the guest in the Treeview
                self.guest_list.selection_set(guest_id_str)
                self.guest_list.focus(guest_id_str)
                self.guest_list.see(guest_id_str)

                # Construct the info message including the total cost
                info_message = (
                    f"ID: {guest_id_str}\n"
                    f"Name: {guest_info['Name']}\n"
                    f"Email: {guest_info['Email']}\n"
                    f"Phone Number: {guest_info['Phone Number']}\n"
                    f"Total Cost: {guest_info.get('Total Cost', 'N/A')}"  # Use get to avoid KeyError
                )

                # Display the guest's information in a message box
                messagebox.showinfo("Guest Information", info_message)
            else:
                messagebox.showerror("Error", f"Guest ID {guest_id_str} not found in the records.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid ID.")
        except tk.TclError:
            messagebox.showerror("Error",
                                 f"Cannot focus on item in the Treeview. Guest ID {guest_id_str} may not exist.")

    def modify_selected_guest(self):
        selected_item = self.guest_list.selection()

        # If nothing is selected, show a messagebox and return
        if not selected_item:
            messagebox.showerror("Error", "No guest selected.")
            return

        selected_item = selected_item[0]  # Focus on first selected item to modify
        guest_info = self.guests[selected_item]

        # Create a new top-level window for editing
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Guest Info")

        # Add entry widgets and populate them with the current guest info
        ttk.Label(edit_window, text="Name:").grid(row=0, column=0)
        name_entry = ttk.Entry(edit_window)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, guest_info["Name"])

        ttk.Label(edit_window, text="Email:").grid(row=1, column=0)
        email_entry = ttk.Entry(edit_window)
        email_entry.grid(row=1, column=1)
        email_entry.insert(0, guest_info["Email"])

        ttk.Label(edit_window, text="Phone Number:").grid(row=2, column=0)
        phone_entry = ttk.Entry(edit_window)
        phone_entry.grid(row=2, column=1)
        phone_entry.insert(0, guest_info["Phone Number"])

        ttk.Label(edit_window, text="Total Cost:").grid(row=3, column=0)
        total_cost_entry = ttk.Entry(edit_window)
        total_cost_entry.grid(row=3, column=1)
        # Use get with a default value to handle missing 'Total Cost' key
        total_cost_entry.insert(0, guest_info.get("Total Cost", "0"))

        def update_guest():
            # Update guest info in the self.guests dictionary
            self.guests[selected_item] = {
                "Name": name_entry.get(),
                "Email": email_entry.get(),
                "Phone Number": phone_entry.get(),
                "Total Cost": total_cost_entry.get()  # Include the total cost
            }

            # Update the Treeview with the new values including the total cost
            self.guest_list.item(selected_item, values=(
                name_entry.get(),
                email_entry.get(),
                phone_entry.get(),
                total_cost_entry.get()  # Add the total cost here
            ))

            # Close the edit window
            edit_window.destroy()

            # Save the updated data to the .pkl file
            self.save_data('../final assignmnet /guests.pkl', self.guests)

        # Button to save changes
        save_button = ttk.Button(edit_window, text="Save Changes", command=update_guest)
        save_button.grid(row=4, column=1, sticky=tk.W)  # Change the row to 4 to avoid overlapping with entries

    def calculate_guest_ui(self, name, email, phone_number):
        self.clear_frame()  # Clear existing widgets
        self.guest_frame = ttk.Frame(self)  # Recreate the frame
        self.guest_frame.pack(fill="both", expand=True)

        lblEvent = ttk.Label(self.guest_frame, text=f"{name}, select your event type:")
        lblEvent.grid(column=0, row=0, sticky='W')
        self.event_type = ttk.Combobox(self.guest_frame, values=["Wedding", "Birthday", "Themed Party", "Graduation"])
        self.event_type.grid(column=1, row=0, sticky='W')

        lblServices = ttk.Label(self.guest_frame, text="Choose additional services:")
        lblServices.grid(column=0, row=1, sticky='W')
        self.chkCatering = ttk.Checkbutton(self.guest_frame, text="Catering ($200)")
        self.chkCatering.grid(column=1, row=1, sticky='W')
        self.chkCleaning = ttk.Checkbutton(self.guest_frame, text="Cleaning ($100)")
        self.chkCleaning.grid(column=1, row=2, sticky='W')
        self.chkDecorations = ttk.Checkbutton(self.guest_frame, text="Decorations ($150)")
        self.chkDecorations.grid(column=1, row=3, sticky='W')

        btnCalculate = ttk.Button(self.guest_frame, text="Calculate Cost", command=lambda: self.calculate_cost(name))
        btnCalculate.grid(column=1, row=4)

    def calculate_cost(self, name):
        base_prices = {
            "Wedding": 1000,
            "Birthday": 500,
            "Themed Party": 750,
            "Graduation": 600
        }
        cost = base_prices.get(self.event_type.get(), 0)
        if self.chkCatering.instate(['selected']):
            cost += 200
        if self.chkCleaning.instate(['selected']):
            cost += 100
        if self.chkDecorations.instate(['selected']):
            cost += 150

        messagebox.showinfo("Event Cost", f"{name}, your total cost is ${cost}.")

    def save_cost(self):
        if hasattr(self, 'selected_guest_id') and self.selected_guest_id:
            try:
                # Convert the input to a float and then back to a string to format as currency
                total_cost_value = float(self.total_cost_entry.get())
                formatted_cost = f"${total_cost_value:.2f}"

                # Update the guests dictionary with the new cost
                self.guests[self.selected_guest_id]['Total Cost'] = formatted_cost

                # Update the Treeview with the new cost
                self.guest_list.item(self.selected_guest_id, values=(
                    self.guests[self.selected_guest_id]["Name"],
                    self.guests[self.selected_guest_id]["Email"],
                    self.guests[self.selected_guest_id]["Phone Number"],
                    formatted_cost
                ))

                # Save the updated data to the .pkl file
                self.save_data('../final assignmnet /guests.pkl', self.guests)
                messagebox.showinfo("Success", "The total cost has been saved.")
            except ValueError:
                messagebox.showerror("Error", "Invalid cost. Please enter a numeric value.")
        else:
            messagebox.showerror("Error", "No guest selected or no cost entered.")

    def on_guest_select(self, event):
        selected = self.guest_list.selection()
        if selected:
            self.selected_guest_id = selected[0]

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


    def event_ui(self):
        self.clear_frame()
        self.event_frame = ttk.Frame(self)
        self.event_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add labels and entry widgets for event details
        ttk.Label(self.event_frame, text="Event Type:").grid(row=0, column=0, sticky=tk.W)

        # Set up the event type ComboBox
        self.event_type_entry = ttk.Combobox(self.event_frame,
                                             values=[event_type.name for event_type in EventType],
                                             state="readonly")
        self.event_type_entry.grid(row=0, column=1)
        self.event_type_entry.current(0)

        ttk.Label(self.event_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
        self.event_date_entry = ttk.Entry(self.event_frame)
        self.event_date_entry.grid(row=1, column=1)

        ttk.Label(self.event_frame, text="Client Name:").grid(row=2, column=0, sticky=tk.W)
        self.client_name_entry = ttk.Entry(self.event_frame)
        self.client_name_entry.grid(row=2, column=1)

        ttk.Label(self.event_frame, text="Venue:").grid(row=3, column=0, sticky=tk.W)
        self.venue_entry = ttk.Entry(self.event_frame)
        self.venue_entry.grid(row=3, column=1)

        # Add buttons for adding, modifying, and deleting events
        ttk.Button(self.event_frame, text="Add Event", command=self.add_event).grid(row=4, columnspan=2, pady=5)
        ttk.Button(self.event_frame, text="Modify Selected Event", command=self.modify_event).grid(row=5, columnspan=2,
                                                                                                   pady=5)
        ttk.Button(self.event_frame, text="Delete Selected Event", command=self.delete_event).grid(row=6, columnspan=2,
                                                                                                   pady=5)

        # Add search functionality
        ttk.Label(self.event_frame, text="Search by Event ID:").grid(row=7, column=0, sticky=tk.W)
        self.search_event_entry = ttk.Entry(self.event_frame)
        self.search_event_entry.grid(row=7, column=1)
        ttk.Button(self.event_frame, text="Search", command=self.search_event).grid(row=7, column=2, padx=5)

        # Initialize the Treeview for the events list
        self.event_list = ttk.Treeview(self.event_frame, columns=("Event Type", "Date", "Client", "Venue"))
        self.event_list.heading("#0", text="Event ID")
        self.event_list.column("#0", width=80)
        for col in ("Event Type", "Date", "Client", "Venue"):
            self.event_list.heading(col, text=col)
            self.event_list.column(col, width=120)
        self.event_list.grid(row=8, column=0, columnspan=3, sticky='nsew')

        # Populate the Treeview with event data
        self.populate_event_list()

        # Bind the selection change event to a handler
        self.event_list.bind("<<TreeviewSelect>>", self.on_event_select)

    def add_event(self):
        # Gather details from the entry fields
        event_type = EventType[self.event_type_entry.get()]
        date = self.event_date_entry.get()
        client_name = self.client_name_entry.get()
        venue = self.venue_entry.get()

        # You would typically validate the input here

        # Generate a new unique event ID
        event_id = str(self.event_id_counter)


        # Create a new event dictionary
        new_event = {
            'Event Type': event_type,
            'Date': date,
            'Client': client_name,
            'Venue': venue
        }

        # Add the new event to the events dictionary
        self.events[event_id] = new_event

        # Update the list displayed to the user
        self.populate_event_list()

    def modify_event(self):
        # Get the selected item in the Treeview
        selected_item = self.event_list.selection()
        if selected_item:
            selected_item = selected_item[0]

            # Gather details from the entry fields
            event_type = self.event_type_entry.get()
            date = self.event_date_entry.get()
            client_name = self.client_name_entry.get()
            venue = self.venue_entry.get()

            # Update the event details in the events dictionary
            self.events[selected_item] = {
                'Event Type': event_type,
                'Date': date,
                'Client': client_name,
                'Venue': venue
            }

            # Update the list displayed to the user
            self.populate_event_list()
        else:
            messagebox.showerror("Error", "No event selected for modification.")

    def delete_event(self):
        # Get the selected item in the Treeview
        selected_item = self.event_list.selection()
        if selected_item:
            selected_item = selected_item[0]

            # Confirm the deletion
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected event?")
            if response:
                # Delete the event from the events dictionary
                del self.events[selected_item]

                # Update the list displayed to the user
                self.populate_event_list()
        else:
            messagebox.showerror("Error", "No event selected for deletion.")

    def search_event(self):
        # Get the event ID from the search entry
        event_id = self.search_event_entry.get()

        # Find the event by ID
        event = self.events.get(event_id)

        if event:
            # Prepare the event information to be displayed
            event_details = "\n".join(f"{key}: {value}" for key, value in event.items())

            # Display a message box with the event details
            messagebox.showinfo("Event Details", f"Event ID {event_id} found:\n\n{event_details}")

            # Clear the current selection in the Treeview
            self.event_list.selection_remove(self.event_list.selection())

            # Select and focus the found event in the Treeview
            self.event_list.selection_set(event_id)
            self.event_list.focus(event_id)
            self.event_list.see(event_id)
        else:
            # This will show an error dialog if the event ID is not found
            messagebox.showerror("Error", f"Event ID {event_id} not found.")

    def populate_event_list(self):
        # Clear the current view
        for item in self.event_list.get_children():
            self.event_list.delete(item)

        # Populate the Treeview with the events from the events dictionary
        for event_id, event in self.events.items():
            self.event_list.insert("", 'end', iid=event_id, text=event_id, values=(
                event['Event Type'].name,  # This now uses the name attribute of the enum
                event['Date'],
                event['Client'],
                event['Venue']
            ))

    def on_event_select(self, event):
        # Get the selected item's ID
        selected_item = self.event_list.selection()
        if selected_item:
            selected_item = selected_item[0]

            # Get the event details and populate the entry fields for editing
            event = self.events[selected_item]
            self.event_type_entry.delete(0, tk.END)
            self.event_type_entry.insert(0, event['Event Type'])
            self.event_date_entry.delete(0, tk.END)
            self.event_date_entry.insert(0, event['Date'])
            self.client_name_entry.delete(0, tk.END)
            self.client_name_entry.insert(0, event['Client'])
            self.venue_entry.delete(0, tk.END)
            self.venue_entry.insert(0, event['Venue'])

        def clear_frame(self):
            # This method will destroy all the widgets in the current frame
            for widget in self.event_frame.winfo_children():
                widget.destroy()
#-----------------------------------------------------------
    def venue_ui(self):
        if hasattr(self, 'venue_frame'):
            self.clear_frame()
        else:
            self.venue_frame = ttk.Frame(self)
            self.venue_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure column widths (allow the second column to expand)
        self.venue_frame.columnconfigure(1, weight=1)

        # Labels and Entries
        ttk.Label(self.venue_frame, text="Venue Name:").grid(row=1, column=0, sticky=tk.W)
        self.venue_name_entry = ttk.Entry(self.venue_frame)
        self.venue_name_entry.grid(row=1, column=1, sticky="ew")  # Make entry expand with the column

        ttk.Label(self.venue_frame, text="Address:").grid(row=2, column=0, sticky=tk.W)
        self.venue_address_entry = ttk.Entry(self.venue_frame)
        self.venue_address_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(self.venue_frame, text="Contact:").grid(row=3, column=0, sticky=tk.W)
        self.venue_contact_entry = ttk.Entry(self.venue_frame)
        self.venue_contact_entry.grid(row=3, column=1, sticky="ew")

        ttk.Label(self.venue_frame, text="Minimum Guests:").grid(row=4, column=0, sticky=tk.W)
        self.venue_min_guests_entry = ttk.Entry(self.venue_frame)
        self.venue_min_guests_entry.grid(row=4, column=1, sticky="ew")

        ttk.Label(self.venue_frame, text="Maximum Guests:").grid(row=5, column=0, sticky=tk.W)
        self.venue_max_guests_entry = ttk.Entry(self.venue_frame)
        self.venue_max_guests_entry.grid(row=5, column=1, sticky="ew")

        # Buttons
        ttk.Button(self.venue_frame, text="Add Venue", command=self.add_venue).grid(row=6, column=0, columnspan=2,
                                                                                    pady=5)
        ttk.Button(self.venue_frame, text="Modify Selected Venue", command=self.modify_venue).grid(row=7, column=0,
                                                                                                   columnspan=2, pady=5)
        ttk.Button(self.venue_frame, text="Delete Selected Venue", command=self.delete_venue).grid(row=8, column=0,
                                                                                                   columnspan=2, pady=5)

        # Search UI
        ttk.Label(self.venue_frame, text="Search Venue ID:").grid(row=10, column=0, sticky=tk.W)
        self.venue_id_search_entry = ttk.Entry(self.venue_frame)
        self.venue_id_search_entry.grid(row=10, column=1)
        ttk.Button(self.venue_frame, text="Search", command=self.search_venue_by_id).grid(row=10, column=2)


        # Treeview
        self.venue_list = ttk.Treeview(self.venue_frame,
                                       columns=("Venue ID", "Name", "Address", "Contact", "Min Guests", "Max Guests"))
        self.venue_list.column("#0", width=0, stretch=tk.NO)
        self.venue_list.heading("#0", text="")
        for col in self.venue_list["columns"]:
            self.venue_list.heading(col, text=col)
            self.venue_list.column(col, width=120)
        self.venue_list.grid(row=9, column=0, columnspan=3, sticky='nsew')  # Make Treeview expand fully

        self.populate_venue_list()


    def on_venue_select(self, event):
        # Code to handle venue selection changes
        selected_item = self.venue_list.selection()[0]
        # Now you can use selected_item to get details or take action

    def add_venue(self):
        # Gather details from the entry fields
        venue_name = self.venue_name_entry.get()
        venue_address = self.venue_address_entry.get()
        venue_contact = self.venue_contact_entry.get()
        venue_min_guests = self.venue_min_guests_entry.get()
        venue_max_guests = self.venue_max_guests_entry.get()

        # Generate a new unique venue ID by incrementing the last ID used
        venue_id = str(self.venue_id_counter)
        # ... code to add the venue ...
        self.venue_id_counter += 1

        # Ensure the order of these values matches the columns in the Treeview
        venue_details = (venue_name, venue_address, venue_contact, venue_min_guests, venue_max_guests)

        # Assuming you have a Venue class that correctly assigns these values
        new_venue = Venue(venue_id, *venue_details)

        # Add the new venue to the venues dictionary, using venue_id as a string
        self.venues[venue_id] = new_venue

        # Update the Treeview with the new venue details
        self.venue_list.insert("", 'end', iid=venue_id,
                               values=(venue_name, venue_address, venue_contact, venue_min_guests, venue_max_guests))

        # Clear the entry fields after adding the venue
        self.clear_venue_entries()

        # Update the list displayed to the user
        self.populate_venue_list()




    def display_venue_details(self, venue_id):
        venue = self.find_venue_by_id(venue_id)
        if venue:
            venue.display_venue_details()
        else:
            messagebox.showerror("Error", "Venue not found.")

    def get_selected_venue_id(self):
        selected_items = self.venue_list.selection()
        if selected_items:  # Ensure there is at least one selected item
            selected_item = selected_items[0]
            return self.venue_list.item(selected_item, 'values')[0]  # Assuming the ID is stored in the first column
        return None

    def search_venue_by_id(self):
        search_id = self.venue_id_search_entry.get()
        venue = self.venues.get(search_id, None)
        if venue:
            # Clear the current selection
            self.venue_list.selection_remove(self.venue_list.selection())
            # Highlight the searched venue
            self.venue_list.selection_set(search_id)
            # Optionally, you can also bring the searched venue into view
            self.venue_list.see(search_id)

            # Prepare the message with venue details
            venue_info = f"Venue ID: {search_id}\n"
            venue_info += f"Name: {venue.name}\n"
            venue_info += f"Address: {venue.address}\n"
            venue_info += f"Contact: {venue.contact}\n"
            venue_info += f"Minimum Guests: {venue.min_guests}\n"
            venue_info += f"Maximum Guests: {venue.max_guests}"

            # Display a messagebox with the venue details
            messagebox.showinfo("Venue Found", venue_info)
        else:
            messagebox.showerror("Error", "Venue not found.")

    def modify_venue(self):
        selected_venue_id = self.get_selected_venue_id()
        if selected_venue_id:
            self.open_modify_venue_window(selected_venue_id)
        else:
            messagebox.showerror("Error", "No venue selected for modification.")


    def edit_venue_ui(self, venue_id):
        # Retrieve the current venue details
        venue = self.venues.get(venue_id)
        if not venue:
            messagebox.showerror("Error", "The selected venue could not be found.")
            return

        # Update the entry fields with the current venue details
        self.venue_name_entry.delete(0, tk.END)
        self.venue_name_entry.insert(0, venue.name)

        self.venue_address_entry.delete(0, tk.END)
        self.venue_address_entry.insert(0, venue.address)

        self.venue_contact_entry.delete(0, tk.END)
        self.venue_contact_entry.insert(0, venue.contact)

        self.venue_min_guests_entry.delete(0, tk.END)
        self.venue_min_guests_entry.insert(0, venue.min_guests)

        self.venue_max_guests_entry.delete(0, tk.END)
        self.venue_max_guests_entry.insert(0, venue.max_guests)

        # If the save_button does not exist, create it
        self.save_button.config(command=lambda: self.save_venue_changes(venue_id))

    def open_modify_venue_window(self, venue_id):
        venue = self.venues.get(venue_id, None)
        if not venue:
            messagebox.showerror("Error", "Venue not found.")
            return

        # Create a new top-level window
        modify_window = tk.Toplevel(self)
        modify_window.title("Modify Venue")

        # Display the venue ID as a reference, but do not allow it to be changed
        ttk.Label(modify_window, text=f"Venue ID: {venue_id}").grid(row=0, column=0, sticky=tk.W)

        # Add entry widgets and labels for venue details
        labels = ["Name", "Address", "Contact", "Minimum Guests", "Maximum Guests"]
        entries = {}

        for i, label in enumerate(labels, start=1):  # Start at row 1
            ttk.Label(modify_window, text=f"{label}:").grid(row=i, column=0, sticky=tk.W)
            entry = ttk.Entry(modify_window)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            entries[label.lower().replace(" ", "_")] = entry

            # Populate the entry fields with the current venue details
        entries['name'].insert(0, venue.name)
        entries['address'].insert(0, venue.address)
        entries['contact'].insert(0, venue.contact)
        entries['minimum_guests'].insert(0, str(venue.min_guests))  # Convert to string if necessary
        entries['maximum_guests'].insert(0, str(venue.max_guests))

        # Save button updates the venue and Treeview, then closes the window
        save_button = ttk.Button(modify_window, text="Save Changes",
                                 command=lambda: self.save_venue_changes(venue_id, entries, modify_window))
        save_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        modify_button = ttk.Button(self.venue_frame, text="Modify Selected Venue",
                                   command=lambda: self.modify_venue())
        modify_button.grid(row=7, column=0, columnspan=2, pady=5)

        # Cancel button closes the window without saving
        cancel_button = ttk.Button(modify_window, text="Cancel", command=modify_window.destroy)
        cancel_button.grid(row=len(labels)+2, column=0, columnspan=2)

        # Make the modify window modal
        modify_window.transient(self)
        modify_window.grab_set()
        self.wait_window(modify_window)

    def save_venue_changes(self, venue_id, entries, modify_window):
        # Fetch the current venue from the dictionary using the existing ID
        venue = self.venues[venue_id]

        # Update the venue details with information from the entry widgets
        venue.name = entries['name'].get()
        venue.address = entries['address'].get()
        venue.contact = entries['contact'].get()
        venue.min_guests = entries['minimum_guests'].get()
        venue.max_guests = entries['maximum_guests'].get()

        # Update the Treeview item; note that the venue ID is not changed here
        self.venue_list.item(venue_id, values=(venue.name, venue.address,
                                               venue.contact, venue.min_guests, venue.max_guests))

        # Save changes to the pickle file; the key, which is the venue ID, remains unchanged
        with open('../final assignmnet /venues.pkl', 'wb') as outfile:
            pickle.dump(self.venues, outfile, pickle.HIGHEST_PROTOCOL)

        # Close the modification window
        modify_window.destroy()

    def delete_venue(self):
        selected_venue_id = self.get_selected_venue_id()
        if selected_venue_id and messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this venue?"):
            # Remove the venue from the system
            if selected_venue_id in self.venues:
                del self.venues[selected_venue_id]
                self.populate_venue_list()  # Refresh the UI
        else:
            messagebox.showerror("Error", "No venue selected or deletion cancelled.")

    def populate_venue_list(self):
        # Clear the existing entries in the Treeview
        self.venue_list.delete(*self.venue_list.get_children())
        # Insert new entries into the Treeview
        for venue_id, venue in self.venues.items():
            # Access attributes directly if 'venue' is an instance of a class
            venue_details = (
                venue_id,
                venue.name,  # Accessing name attribute
                venue.address,  # Accessing address attribute
                venue.contact,  # Accessing contact attribute
                venue.min_guests,  # Accessing minimum guests attribute
                venue.max_guests  # Accessing maximum guests attribute
            )
            self.venue_list.insert("", 'end', iid=venue_id, values=venue_details)

    def clear_venue_entries(self):
        # Assuming you have entry fields named 'venue_name_entry', 'venue_address_entry', etc.
        self.venue_name_entry.delete(0, 'end')
        self.venue_address_entry.delete(0, 'end')
        self.venue_contact_entry.delete(0, 'end')
        self.venue_min_guests_entry.delete(0, 'end')
        self.venue_max_guests_entry.delete(0, 'end')




if __name__ == "__main__":
    app = EventManagementApp()
    app.mainloop()
