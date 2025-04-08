import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from google.cloud import bigquery
from ttkbootstrap.validation import add_regex_validation
import AddAudit 
import AddFile 
import AddRequest
import logging

class MenuM(ttk.Frame):
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

        self.pack(fill=BOTH, expand=YES)
        self.create_dropdown_menu()
        self.data = []
       
        self.colors = master_window.style.colors

        self.create_buttonbox()  

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
			text="Add New Audit",
			command=self.openAuditNewWindow,
			bootstyle=SUCCESS,
			width=15,
		)
        Audit_btn.pack(side=LEFT, padx=5)
        
    def create_dropdown_menu(self):
        navbar = ttk.Frame(self, padding=(10, 5))
        navbar.pack(fill=X, side=TOP)

        menu_button = ttk.Menubutton(navbar, text="☰ Menu", bootstyle="info-outline", width=10)
        menu = ttk.Menu(menu_button, tearoff=0)
        menu_button.config(menu=menu)

        menu.add_command(label="📩 Add Request", command=self.openRequestNewWindow)
        menu.add_command(label="📋 Add Management Reaponse", command=self.openMangementNewWindow)
        menu.add_command(label="📊 Add Risk Matrix", command=self.openRiskNewWindow)
        menu.add_separator()
        menu.add_command(label="📉 Reporting", background="purple", command=self.openExportNewWindow)         
        

        menu_button.pack(side=RIGHT)           
    
    def ensure_dataset_exists(self,client, dataset_id):
        """Ensure that a BigQuery dataset exists."""
        try:
            client.get_dataset(dataset_id)  # Attempt to fetch the dataset
            print(f"Dataset {dataset_id} already exists.")
        except bigquery.NotFound:
            # Dataset not found; create it
            print(f"Database don't exists {dataset_id}.")
    
    def create_table(self):
        coldata = [
            {"text": "Audit ID", "stretch": False},
            {"text": "Auditor Name"},
            {"text": "Audit Project"},
            {"text": "Epic"},
            {"text": "UserStory"},
            {"text": "Division Name"},
            {"text": "Department"},
            {"text": "FY - Quarter"},
            {"text": "Audit Status"},
            {"text": "Audit Start Date"},
            {"text": "Audit End Date"},
            {"text": "Audit Actual Delivered Date"},
            
        ]

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
    
    def fetch_existing_data(self): 
        if not self.bigquery_client:
            print("BigQuery client not available. Skipping data fetch.")
            return
    
        query = """
            SELECT 
                ap.audit_id
                ,a.auditor_name
                ,ap.audit_project
                ,ap.epic
                ,ap.userstory
                ,d.division_name
                ,d.department
                ,ap.fy_quarter
                ,ap.status_of_audit
                ,ap.audit_start_date
                ,ap.date_for_deliverable
                ,ap.actual_date_delivered 
            FROM `audit-447319.Audits.Audit_Program` ap
                JOIN `audit-447319.Audits.Auditor` a on ap.auditor_id = a.auditor_id  
                JOIN `audit-447319.Audits.Division` d on ap.division_id = d.division_id
            where 
                status_of_audit = 'In Progress'"""     
        
        try:
            results = self.bigquery_client.query(query)
            self.data = [(
            row["audit_id"],
            row["auditor_name"],
            row["audit_project"],
            row["epic"],
            row["userstory"],
            row["division_name"],
            row["department"],
            row["fy_quarter"],
            row["status_of_audit"],
            row["audit_start_date"],
            row["date_for_deliverable"],
            row["actual_date_delivered"],
            ) 
            for row in results
            ]
            print(f"Fetched data: {self.data}")  # Debugging log
        except Exception as e:
            print(f"Failed to fetch data: {e}")
                   
    def openAuditNewWindow(self):
        app1 = ttk.Toplevel("Enter New Audit", "superhero", resizable=(True, True))
        AddAudit.Audit(app1)
        app1.mainloop()
        
    def openRequestNewWindow(self):
        app1 = ttk.Toplevel("Enter Request", "darkly", resizable=(True, True))
        AddRequest.Request(app1)
        app1.mainloop()
        
    def openMangementNewWindow(self):
        app1 = ttk.Toplevel("Enter Managemnet Response", "superhero", resizable=(True, True))
        AddFile.File(app1)
        app1.mainloop()
        
    def openRiskNewWindow(self):
        app1 = ttk.Toplevel("Enter Risks", "superhero", resizable=(True, True))
        AddRequest.Request(app1)
        app1.mainloop()
        
    def openExportNewWindow(self):
        app1 = ttk.Toplevel("Export Date", "superhero", resizable=(True, True))
        AddRequest.Request(app1)
        app1.mainloop()    
    # def on_submit():
    #     pass # an empty function definition



