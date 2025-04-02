import os 
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from datetime import datetime
import db
import logging

class Request(ttk.Frame):
       
    def __init__(self, master_window2):
        super().__init__(master_window2, padding=(20,10))
        master_window2.geometry("900x700")  # 800x600 is the size
        
        try:
            self.bigquery_client = bigquery.Client()
            dataset_id = "audit-447319.Audits"  # Replace with your project_id and dataset name
            self.ensure_dataset_exists(self.bigquery_client, dataset_id)
        except Exception as e:
            self.bigquery_client = None
            print(f"Failed to initialize BigQuery client or ensure dataset existence: {e}")
        
        dataset_id = "audit-447319.Audits"
        table_id = "Request"
        
        if self.bigquery_client:
            self.create_table_if_not_exists(self.bigquery_client, dataset_id, table_id)
        
        self.pack(fill=BOTH, expand=YES)
        
        # Initialize StringVars
        self.request_id = ttk.StringVar(value="")
        self.file_id = ttk.StringVar(value="")
        self.file_name = ttk.StringVar(value="")
        self.request_description = ttk.StringVar(value="")
        self.department_requested = ttk.StringVar(value="")
        self.request_status = ttk.StringVar()  # For combo box
        
        self.some_variable = ttk.StringVar()
        self.request_status = ttk.StringVar()
        
        self.data = []
                   
         # Instruction label
        instruction_text = "Please enter your Request information: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)
             
        # self.create_form_entry("Request ID: ", self.request_id)
        # self.create_form_entry("File ID: ", self.file_id)
        # self.create_form_entry("File Name: ", self.file_name)
        self.create_horizontal_entries()
        
        # Create a shared container
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=10)
        
        self.create_form_entry(container, "Department Requested:", self.some_variable, regex=r'^[a-zA-Z0-9_]*$')
        self.create_form_combo(container, "Request Status:", self.request_status, ["Active", "Suspended", "Closed"])                  
        # self.requested_date = self.create_form_Date("File Requested Date: ")
        # self.received_date = self.create_form_Date("File Received Date: ")
        self.create_horizontal_dates()
        self.comment_box = self.create_comment_box("Request Description:")
        # self.create_form_entry("Request Description: ", self.request_description)
              
        # Colors from master style
        self.colors = master_window2.style.colors
        
        # Submit button
        self.create_buttonbox()

        # # Table
        if self.bigquery_client:
            self.fetch_existing_data()
            self.table = self.create_table()
        else:
            print("BigQuery client not initialized. Data fetching skipped.")  
    
     #**************************COMPONENTS CREATION***************************  
    def create_horizontal_entries(self):
        # Create a container for horizontal alignment
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        # Request ID Label and Entry
        request_id_label = ttk.Label(container, text="Request ID:", width=10)
        request_id_label.pack(side=LEFT, padx=5)
        request_id_entry = ttk.Entry(container, textvariable=self.request_id)
        request_id_entry.pack(side=LEFT, padx=5)

        # File ID Label and Entry
        file_id_label = ttk.Label(container, text="File ID:", width=10)
        file_id_label.pack(side=LEFT, padx=5)  # Additional padding for spacing
        file_id_entry = ttk.Entry(container, textvariable=self.file_id)
        file_id_entry.pack(side=LEFT, padx=5)

        # File Name Label and Entry
        file_name_label = ttk.Label(container, text="File Name:", width=10)
        file_name_label.pack(side=LEFT, padx=5)  # Additional padding for spacing
        file_name_entry = ttk.Entry(container, textvariable=self.file_name)
        file_name_entry.pack(side=LEFT, padx=5)
    
    def create_form_entry(self, parent,label,variable,regex=None):
        # form_field_container = ttk.Frame(self)
        # form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(master=parent, text=label, width=25)
        form_field_label.pack(side=LEFT, padx=5)

        form_input = ttk.Entry(master=parent, textvariable=variable)
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')

        return form_input
    
    def create_form_combo(self, parent,label,variable,values):
        
        # form_field_container = ttk.Frame(self)
        # form_field_container.pack(fill=NONE, expand=NO, pady=5)

        form_field_label = ttk.Label(master=parent, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=5)
                
        form_input = ttk.Combobox(master=parent,textvariable=variable, values= values, state="readonly")
        form_input.pack(side=LEFT, padx=5, fill=NONE, expand=NO)
        
        return form_input
    
    # def add_regex_validation(self, entry, regex):
    #         """
    #     Adds regex validation to an entry widget.
    #     """
    #     def validate_input(event):
    #         value = entry.get()
    #         if not re.match(regex, value):
    #             entry.configure(foreground="red")
    #         else:
    #             entry.configure(foreground="black")
        
    # entry.bind("<KeyRelease>", validate_input)
    
    def create_horizontal_dates(self):
        # Create a container for horizontal alignment
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        # Audit Start Date Label and Entry
        requested_date_label = ttk.Label(container, text="Requested Date:", width=15)
        requested_date_label.pack(side=LEFT, padx=5)
        self.requested_date_entry = ttk.DateEntry(container)
        self.requested_date_entry.pack(side=LEFT, padx=5)

        # Audit End Date Label and Entry
        received_date_label = ttk.Label(container, text="Received Date:", width=15)
        received_date_label.pack(side=LEFT, padx=5)
        self.received_date_entry = ttk.DateEntry(container)
        self.received_date_entry.pack(side=LEFT, padx=5)
    
    def create_comment_box(self, label_text):
        # Create a container for the comment box
        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=YES, pady=5)

        # Label for the comment box
        label = ttk.Label(container, text=label_text, width=25)
        label.pack(side=TOP, anchor=W, padx=5, pady=(0, 5))

        # Text widget for multiline comments
        comment_box = ttk.Text(container, height=5, width=50, wrap=WORD)
        comment_box.pack(fill=BOTH, expand=YES, padx=5)

        return comment_box
    
    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        cancel_btn = ttk.Button(
            master=button_container,
            text="Cancel",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )

        cancel_btn.pack(side=RIGHT, padx=5)

        submit_btn = ttk.Button(
            master=button_container,
            text="Submit",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )

        submit_btn.pack(side=RIGHT, padx=5)
    
    #**************************DATA VERIFICATION CREATION***************************     
    def ensure_dataset_exists(self,client, dataset_id):
        """Ensure that a BigQuery dataset exists."""
        try:
            client.get_dataset(dataset_id)  # Attempt to fetch the dataset
            print(f"Dataset {dataset_id} already exists.")
        except Exception as e:
            if isinstance(e, bigquery.exceptions.NotFound):
                dataset = bigquery.Dataset(dataset_id)
                client.create_dataset(dataset)
                print(f"Created dataset {dataset_id}.")
            else:
                print(f"An error occurred while checking or creating the dataset: {e}")
    
    def fetch_existing_data(self): 
        if not self.bigquery_client:
            print("BigQuery client not available. Skipping data fetch.")
            return
    
        query = "SELECT * FROM `audit-447319.Audits.Request`"
        try:
            results = self.bigquery_client.query(query)
            self.data = [(    
            {"text": "Request ID", "stretch": False},
            {"text": "File ID"},
            {"text": "File Name"},
            {"text": "Department Requested from"},
            {"text": "Request Description"},
            {"text": "Request Status"},
            {"text": "File Requested Date"},
            {"text": "File Received Date"},
            ) 
            for row in results
            ]
            print(f"Fetched data: {self.data}")  # Debugging log
            self.update_table()
        except Exception as e:
            print(f"Failed to fetch data: {e}")

    def create_table_if_not_exists(self, client, dataset_id, table_id):
        """Creates a table if it does not already exist."""
        table_ref = f"{dataset_id}.{table_id}"
        try:
            # Attempt to fetch the table
            client.get_table(table_ref)
            print(f"Table {table_ref} already exists.")
        except NotFound:
            print(f"Table {table_ref} not found. Creating...")
            schema = [
                    bigquery.SchemaField("request_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("file_name", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("file_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("department_requested", "STRING"),
                    bigquery.SchemaField("request_description", "STRING"),
                    bigquery.SchemaField("request_status", "STRING"),
                    bigquery.SchemaField("requested_date", "DATE"),
                    bigquery.SchemaField("received_date", "DATE"),
                ]
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)
            print(f"Table {table_ref} created successfully.")       
    
    #**************************TABLE CREATION***************************    
    def create_table(self):
        coldata = [
            {"text": "Request ID", "stretch": False},
            {"text": "File ID"},
            {"text": "File Name"},
            {"text": "Department Requested from"},
            {"text": "Request Description"},
            {"text": "Request Status"},
            {"text": "File Requested Date"},
            {"text": "File Received Date"},
        ]

        print(self.data)
        
        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            autofit=True,
            bootstyle=PRIMARY,
            # stripecolor=(self.colors.light, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

    def insert_audit_data(self, request_id, file_name, file_id, department_requested, 
                      request_description, request_status, 
                      requested_date, received_date):
       
        if not self.bigquery_client:
            print("BigQuery client not available. Insert operation aborted.")
            return
       
        """Insert data into the BigQuery Audit table."""
        table_id = "audit-447319.Audits.Request"  # Update with your correct table_id

         # Data to insert
        row_data = {
            "request_id": request_id,
            "file_name": file_name,
            "file_id": file_id,
            "department_requested": department_requested,
            "request_description": request_description,
            "request_status": request_status,
            "requested_date": requested_date,
            "received_date": received_date,
        }

        try:
            # Insert data into BigQuery
            errors = self.bigquery_client.insert_rows_json(table_id, [row_data])
            if not errors:
                print("Data inserted successfully into BigQuery.")
            else:
                print(f"Failed to insert data: {errors}")
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
    
    def update_table(self):
        """Update the Tableview with the current data."""
        if not hasattr(self, "table") or self.table is None:
            print("Table not initialized. Skipping update.")
            return
        # Update table rows
        self.table.delete_rows()  # Clear existing rows
        if self.data:  # Ensure there is data to insert
            self.table.insert_rows(index=0,rowdata=self.data)  # Pass data as rowdata
    
     #**************************COMPONENTS FUNCTION*************************** 
    def on_submit(self):
        """Print the contents to console and return the values."""  
        try:
            request_id = self.request_id.get()
            file_name = self.file_name.get()
            file_id = self.file_id.get()
            # audit_description = self.audit_description.get()
            request_description = self.comment_box.get("1.0", "end").strip()
            department_requested = self.department_requested.get()
            request_status = self.request_status.get()
            requested_date = self.requested_date_entry.entry.get()
            received_date = self.received_date_entry.entry.get()
       
            # Ensure required fields are filled
            if not all([request_id, file_name, file_id, department_requested]):
                raise ValueError("All fields are required.")

            # Parse and validate dates
            requested_date = datetime.strptime(requested_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            received_date = datetime.strptime(received_date, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Check for duplicates
            if any(row[0] == request_id for row in self.data):
                raise ValueError("Request ID already exists.")

            # Insert data into BigQuery
            self.insert_audit_data(
                request_id=request_id,
                file_name=file_name,
                file_id=file_id,
                department_requested=department_requested,
                request_description=request_description,
                request_status=request_status,
                requested_date=requested_date,
                received_date=received_date,
            )

            # Update table
            self.data.append(
                (request_id, file_name, file_id, department_requested,request_description, request_status, 
                      requested_date, received_date)
            )
            
            self.update_table()
            self.table.destroy()
            self.table = self.create_table()

            # Success message
            ToastNotification(
                title="Success!",
                message="Request data submitted successfully.",
                duration=3000,
                bootstyle=SUCCESS,
            ).show_toast()

        except ValueError as ve:
            ToastNotification(
                title="Submission Failed!",
                message=str(ve),
                duration=3000,
                bootstyle=DANGER,
            ).show_toast()

        except Exception as e:
            ToastNotification(
                title="Submission Failed!",
                message=f"An unexpected error occurred: {str(e)}",
                duration=3000,
                bootstyle=DANGER,
            ).show_toast()

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()

    
