import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from google.cloud import bigquery
from ttkbootstrap.validation import add_regex_validation
import AddAudit 
import AddFile 
import AddRequest
import logging

class Menu(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20,10))
    
        # Center the window
        master_window.geometry("800x600")  # 800x600 is the size
        master_window.title("Menu")
        master_window.resizable(True, True)  # Disable resizing

        try:
            self.bigquery_client = bigquery.Client()
            dataset_id = "audit-447319.Audits"  # Replace with your project_id and dataset name
            AddAudit.Audit.ensure_dataset_exists(self,self.bigquery_client, dataset_id)
        except Exception as e:
            self.bigquery_client = None
            print(f"Failed to initialize BigQuery client or ensure dataset existence: {e}")
        
        # Add widgets or other initialization code here
        instruction = ttk.Label(master_window, text="Welcome to the Menu!", bootstyle="primary")
        instruction.pack(pady=10)

        self.pack(fill=BOTH, expand=YES)
        
        self.data = []
       
        self.colors = master_window.style.colors

        instruction_text = "Please enter your audit information: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)

        self.create_buttonbox()  
        
        instruction_text1 = "Active Audits: " 
        instruction = ttk.Label(self, text=instruction_text1, width=50)
        instruction.pack(fill=X, pady=10)

        if self.bigquery_client:
            self.fetch_existing_data()
            self.table = self.create_table()
        else:
            print("BigQuery client not initialized. Data fetching skipped.") 
        
    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=NO, pady=(15, 10))
        
        Audit_btn = ttk.Button(
			master=button_container,
			text="Add Audit",
			command=self.openAuditNewWindow,
			bootstyle=SUCCESS,
			width=15,
		)
        Audit_btn.pack(side=LEFT, padx=5)
        
        File_btn = ttk.Button(
            master=button_container,
            text="Add File",
            command=self.openFileNewWindow,
            bootstyle=SUCCESS,
            width=15,
        )

        File_btn.pack(side=LEFT, padx=5)

        Request_btn = ttk.Button(
            master=button_container,
            text="Add Request",
            command=self.openRequestNewWindow,
            bootstyle=SUCCESS,
            width=15,
        )

        Request_btn.pack(side=LEFT, padx=5)
    
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

        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            # stripecolor=(self.colors.light, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table
    
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
    
        query = "SELECT * FROM `audit-447319.Audits.Audit` where audit_status = 'Active' "
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
        except Exception as e:
            print(f"Failed to fetch data: {e}")
                   
    def openAuditNewWindow(self):
        app1 = ttk.Toplevel("Enter Audit", "superhero", resizable=(True, True))
        AddAudit.Audit(app1)
        app1.mainloop()
        
    def openFileNewWindow(self):
        app1 = ttk.Toplevel("Enter File", "superhero", resizable=(True, True))
        AddFile.File(app1)
        app1.mainloop()
        
    def openRequestNewWindow(self):
        app1 = ttk.Toplevel("Enter Request", "superhero", resizable=(True, True))
        AddRequest.Request(app1)
        app1.mainloop()
        
    # def on_submit():
    #     pass # an empty function definition



