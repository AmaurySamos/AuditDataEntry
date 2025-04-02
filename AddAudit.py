import os 
from google.cloud import bigquery
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from datetime import datetime
import db
##import logging

class Audit(ttk.Frame):
       
    def __init__(self, master_window2):
        super().__init__(master_window2, padding=(20,10))
        master_window2.geometry("900x700")  # 800x600 is the size
        # master_window2.title("ADD AUDIT")
        # master_window2.resizable(True, True)  # Disable resizing
                
        try:
            self.bigquery_client = bigquery.Client()
            dataset_id = "audit-447319.Audits"  # Replace with your project_id and dataset name
            self.ensure_dataset_exists(self.bigquery_client, dataset_id)
        except Exception as e:
            self.bigquery_client = None
            print(f"Failed to initialize BigQuery client or ensure dataset existence: {e}")
        
        dataset_id = "audit-447319.Audits"
        table_id = "Audit"
        self.create_table_if_not_exists(self.bigquery_client, dataset_id, table_id)  
        
        self.pack(fill=BOTH, expand=YES) 
                
        # Initialize StringVars
        self.audit_id = ttk.StringVar(value="")
        self.audit_name = ttk.StringVar(value="")
        self.auditor_id = ttk.StringVar(value="")
        self.audit_description = ttk.StringVar(value="")
        self.audit_importance_level = ttk.StringVar()  # For combo box
        self.audit_status = ttk.StringVar()  # For combo box
                
        self.data = []
       
        # Instruction label
        instruction_text = "Please enter your audit information: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)
       
        # self.create_form_entry("Audit ID: ", self.audit_id)
        # self.create_form_entry("Audit Name: ", self.audit_name)
        self.create_horizontal_entries()
        # self.create_form_entry("Auditor ID: ", self.auditor_id)
        # self.create_form_entry("Audit Description: ", self.audit_description)
        self.create_form_combo()     
        self.create_horizontal_dates()
        self.comment_box = self.create_comment_box("Audit Description:")

        # self.audit_start_date_entry = self.create_form_Date("Audit Start Date: ")
        # self.audit_end_date_entry = self.create_form_Date("Audit End Date: ")
        # self.audit_actual_end_date_entry = self.create_form_Date("Audit Actual Date: ") 
        
        # Colors from master style
        self.colors = master_window2.style.colors
        
        # Submit button
        self.create_buttonbox()
        
        if self.bigquery_client:
            self.fetch_existing_data()
            self.table = self.create_table()
        else:
            print("BigQuery client not initialized. Data fetching skipped.")     
               
    #**************************COMPONENTS CREATION***************************      
   
    def create_horizontal_entries(self):
        # Create a container for horizontal alignment
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=10)

        # Audit ID Label and Entry
        audit_id_label = ttk.Label(container, text="Audit ID:", width=15)
        audit_id_label.pack(side=LEFT, padx=5)
        audit_id_entry = ttk.Entry(container, textvariable=self.audit_id)
        audit_id_entry.pack(side=LEFT, padx=5)

        # Audit Name Label and Entry
        audit_name_label = ttk.Label(container, text="Audit Name:", width=15)
        audit_name_label.pack(side=LEFT, padx=5)  # Additional padding for spacing
        audit_name_entry = ttk.Entry(container, textvariable=self.audit_name)
        audit_name_entry.pack(side=LEFT, padx=5)

        # Auditor ID Label and Entry
        auditor_id_label = ttk.Label(container, text="Auditor ID:", width=15)
        auditor_id_label.pack(side=LEFT, padx=5)  # Additional padding for spacing
        auditor_id_label = ttk.Entry(container, textvariable=self.auditor_id)
        auditor_id_label.pack(side=LEFT, padx=5)
   
        # add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')
        
    def create_horizontal_dates(self):
        # Create a container for horizontal alignment
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=10)

        # Audit Start Date Label and Entry
        audit_start_date_label = ttk.Label(container, text="Audit Start Date:", width=15)
        audit_start_date_label.pack(side=LEFT, padx=5)
        self.audit_start_date_entry = ttk.DateEntry(container)
        self.audit_start_date_entry.pack(side=LEFT, padx=5)

        # Audit End Date Label and Entry
        audit_end_date_label = ttk.Label(container, text="Audit End Date:", width=15)
        audit_end_date_label.pack(side=LEFT, padx=5)
        self.audit_end_date_entry = ttk.DateEntry(container)
        self.audit_end_date_entry.pack(side=LEFT, padx=5)

        # Audit Actual End Date Label and Entry
        audit_actual_end_date_label = ttk.Label(container, text="Audit Actual Date:", width=15)
        audit_actual_end_date_label.pack(side=LEFT, padx=5)
        self.audit_actual_end_date_entry = ttk.DateEntry(container)
        self.audit_actual_end_date_entry.pack(side=LEFT, padx=5)

    def create_comment_box(self, label_text):
        # Create a container for the comment box
        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=YES, pady=10)

        # Label for the comment box
        label = ttk.Label(container, text=label_text, width=15)
        label.pack(side=TOP, anchor=W, padx=5, pady=(0, 5))

        # Text widget for multiline comments
        comment_box = ttk.Text(container, height=5, width=50, wrap=WORD)
        comment_box.pack(fill=BOTH, expand=YES, padx=5)

        return comment_box

   
    # def create_form_entry(self, label, variable):
    #     form_field_container = ttk.Frame(self)
    #     form_field_container.pack(fill=X, expand=NO, pady=5)

    #     form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
    #     form_field_label.pack(side=LEFT, padx=5)

    #     form_input = ttk.Entry(master=form_field_container, textvariable=variable)
    #     form_input.pack(side=LEFT, padx=5, fill=X, expand=NO)

    #     add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')
    #     return form_input
    
    # def create_form_Date(self, label):
    #     form_field_container = ttk.Frame(self)
    #     form_field_container.pack(fill=X, expand=YES, pady=5)

    #     form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
    #     form_field_label.pack(side=LEFT, padx=12)

    #     form_input = ttk.DateEntry(master=form_field_container)
    #     form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

    #     return form_input
    
    def create_form_combo(self):
            
        combo_container = ttk.Frame(self)
        combo_container.pack(fill=X, pady=10)
 
        # Combo box 1
        label2 = ttk.Label(combo_container, text="Audit Status: ", width=15)
        label2.pack(side=LEFT, padx=5)

        self.category2 = ttk.StringVar()
        combo2 = ttk.Combobox(
            combo_container,
            textvariable=self.audit_status,
            values=["Active", "suspended", "Closed"],  # Add your options
            state="readonly",
        )
        combo2.pack(side=LEFT, padx=5)
        
        # Combo box 2
        label1 = ttk.Label(combo_container, text="Audit Importance: ", width=18)
        label1.pack(side=LEFT, padx=5)

        self.category1 = ttk.StringVar()
        combo1 = ttk.Combobox(
            combo_container,
            textvariable=self.audit_importance_level,
            values=["High", "Medium", "Low"],  # Add your options
            state="readonly",
        )
        combo1.pack(side=LEFT, padx=5)
    
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
        except bigquery.NotFound:
            # Dataset not found; create it
            dataset = bigquery.Dataset(dataset_id)
            dataset = client.create_dataset(dataset)  # Make an API request
            print(f"Created dataset {dataset_id}.")
    
    def fetch_existing_data(self): 
        if not self.bigquery_client:
            print("BigQuery client not available. Skipping data fetch.")
            return
    
        query = "SELECT * FROM `audit-447319.Audits.Audit`"
        try:
            results = self.bigquery_client.query(query)
            self.data = [(
            row["audit_id"],
            row["audit_name"],
            row["auditor_id"],
            row["audit_description"],
            row["audit_importance_level"],
            row["audit_status"],
            row["audit_start_date"],
            row["audit_end_date"],
            row["audit_actual_end_date"],
            ) 
            for row in results
            ]
            print(f"Fetched data: {self.data}")  # Debugging log
            self.update_table()
        except Exception as e:
            print(f"Failed to fetch data: {e}")
        
    def create_table_if_not_exists(self,client, dataset_id, table_id):
        """Ensure a BigQuery table exists."""
        try:
            table_ref = f"{dataset_id}.{table_id}"
            client.get_table(table_ref)  # Try fetching the table
            print(f"Table {table_ref} already exists.")
        except bigquery.NotFound:
            schema = [
                bigquery.SchemaField("audit_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("audit_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("auditor_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("audit_description", "STRING"),
                bigquery.SchemaField("audit_importance_level", "STRING"),
                bigquery.SchemaField("audit_status", "STRING"),
                bigquery.SchemaField("audit_start_date", "DATE"),
                bigquery.SchemaField("audit_end_date", "DATE"),
                bigquery.SchemaField("audit_actual_end_date", "DATE"),
            ]
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)  # Make an API request
            print(f"Created table {table_ref}.")

     #**************************TABLE CREATION*************************** 
    def create_table(self):
        coldata = [
            {"text": "Audit ID", "stretch": False},
            {"text": "Audit Name"},
            {"text": "Auditor ID"},
            {"text": "Audit Description"},
            {"text": "Audit Importance Level"},
            {"text": "Audit Status"},
            {"text": "Audit Start Date"},
            {"text": "Audit End Date"},
            {"text": "Audit Actual End Date"},
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

    def insert_audit_data(self, audit_id, audit_name, auditor_id, audit_description, 
                      audit_importance_level, audit_status, 
                      audit_start_date, audit_end_date, audit_actual_end_date):
       
        if not self.bigquery_client:
            print("BigQuery client not available. Insert operation aborted.")
            return
       
        """Insert data into the BigQuery Audit table."""
        table_id = "audit-447319.Audits.Audit"  # Update with your correct table_id

        # Data to insert
        row_data = {
            "audit_id": audit_id,
            "audit_name": audit_name,
            "auditor_id": auditor_id,
            "audit_description": audit_description,
            "audit_importance_level": audit_importance_level,
            "audit_status": audit_status,
            "audit_start_date": audit_start_date,
            "audit_end_date": audit_end_date,
            "audit_actual_end_date": audit_actual_end_date,
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
            audit_id = self.audit_id.get()
            audit_name = self.audit_name.get()
            auditor_id = self.auditor_id.get()
            # audit_description = self.audit_description.get()
            audit_description = self.comment_box.get("1.0", "end").strip()
            audit_importance_level = self.audit_importance_level.get()
            audit_status = self.audit_status.get()
            audit_start_date = self.audit_start_date_entry.entry.get()
            audit_end_date = self.audit_end_date_entry.entry.get()
            audit_actual_end_date = self.audit_actual_end_date_entry.entry.get()

            # Ensure required fields are filled
            if not all([audit_id, audit_name, auditor_id, audit_description]):
                raise ValueError("All fields are required.")

            # Parse and validate dates
            audit_start_date = datetime.strptime(audit_start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            audit_end_date = datetime.strptime(audit_end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            audit_actual_end_date = datetime.strptime(audit_actual_end_date, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Check for duplicates
            if any(row[0] == audit_id for row in self.data):
                raise ValueError("Audit ID already exists.")

            # Insert data into BigQuery
            self.insert_audit_data(
                audit_id=audit_id,
                audit_name=audit_name,
                auditor_id=auditor_id,
                audit_description=audit_description,
                audit_importance_level=audit_importance_level,
                audit_status=audit_status,
                audit_start_date=audit_start_date,
                audit_end_date=audit_end_date,
                audit_actual_end_date=audit_actual_end_date,
            )

            # Update table
            self.data.append(
                (audit_id, audit_name, auditor_id, audit_description, audit_importance_level,
                audit_status, audit_start_date, audit_end_date, audit_actual_end_date)
            )
            
            self.update_table()
            self.table.destroy()
            self.table = self.create_table()

            # Success message
            ToastNotification(
                title="Success!",
                message="Audit data submitted successfully.",
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
        
