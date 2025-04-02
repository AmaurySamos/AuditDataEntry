from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from datetime import date

class File(ttk.Frame):
       
    def __init__(self, master_window2):
        super().__init__(master_window2, padding=(20,10))
        self.pack(fill=BOTH, expand=YES)
        
        # Initialize StringVars
        self.file_id = ttk.StringVar(value="")
        self.audit_id = ttk.StringVar(value="")
        self.file_name = ttk.StringVar(value="")
        self.file_description = ttk.StringVar(value="")
        self.department_requested = ttk.StringVar(value="")
        self.file_importance = ttk.StringVar()  # For combo box
        self.file_status = ttk.StringVar()  # For combo box
              
         # Instruction label
        instruction_text = "Please enter your File information: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)
       
        self.create_form_entry("File Name: ", self.file_name)
        self.create_form_entry("File ID: ", self.file_id)
        self.create_form_entry("Audit ID: ", self.audit_id)
        self.create_form_entry("Department Requested From: ", self.department_requested)      
        self.create_form_entry("File Description: ", self.file_description)
        
        self.create_form_combo()      
                       
        self.requested_date = self.create_form_Date("File Requested Date: ")

        self.data = []
        
        # Colors from master style
        self.colors = master_window2.style.colors
        
        # Submit button
        self.create_buttonbox()

        # # Table
        self.table = self.create_table()
    
    def create_form_entry(self, label, variable):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=12)

        form_input = ttk.Entry(master=form_field_container, textvariable=variable)
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')

        return form_input
    
    def create_form_Date(self, label):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=12)

        form_input = ttk.DateEntry(master=form_field_container)
        form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

        return form_input
    
    def create_form_combo(self):
        
        combo_container = ttk.Frame(self)
        combo_container.pack(fill=X, pady=10)

        # Combo box 1
        label1 = ttk.Label(combo_container, text="File Importance: ", width=15)
        label1.pack(side=LEFT, padx=5)

        self.category1 = ttk.StringVar()
        combo1 = ttk.Combobox(
            combo_container,
            textvariable=self.file_importance,
            values=["High", "Medium", "Low"],  # Add your options
            state="readonly",
        )
        combo1.pack(side=LEFT, padx=5)

        # Combo box 2
        label2 = ttk.Label(combo_container, text="File Status: ", width=15)
        label2.pack(side=LEFT, padx=5)

        self.category2 = ttk.StringVar()
        combo2 = ttk.Combobox(
            combo_container,
            textvariable=self.file_status,
            values=["Active", "suspended", "Closed"],  # Add your options
            state="readonly",
        )
        combo2.pack(side=LEFT, padx=5)
                            
    # def create_form_combo1(self, label,options):
        
    #     form_field_container = ttk.Frame(self)
    #     form_field_container.pack(fill=NONE, expand=NO, pady=5)

    #     form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
    #     form_field_label.pack(side=TOP, padx=12)
                
    #     form_input = ttk.Combobox(master=form_field_container,textvariable=self.file_status, values= options, state="readonly")
    #     form_input.pack(side=LEFT, padx=5, fill=NONE, expand=YES)
        
    #     return form_input
    
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
    
    def create_table(self):
        coldata = [
            {"text": "File ID"},
            {"text": "Audit ID", "stretch": False},
            {"text": "File Name"},
            {"text": "File Status"},
            {"text": "File Importance"},
            {"text": "File Description"},
            {"text": "Department Requested from"},      
            {"text": "File Requested Date"},
        ]

        # print(self.data)

        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

    def on_submit(self):
        """Print the contents to console and return the values."""
        file_id = self.file_id.get()
        audit_id = self.audit_id.get()
        file_name = self.file_name.get()
        file_status = self.file_status.get()
        file_importance = self.file_importance.get()
        file_description = self.file_description.get()
        department_requested = self.department_requested.get()     
        
        # Use cget("text") to retrieve date values
        requested_date = self.requested_date.entry.get()

        print("File ID:", file_id)
        print("Audit ID: ", audit_id)
        print("File Name:", file_name)
        print("File Status: ", file_status)
        print("File Importance: ", file_importance)
        print("File Description: ", file_description)
        print("Deparment Requested From: ", department_requested)
        print("File Requested Date:", requested_date)

        toast = ToastNotification(
        title="Submission successful!",
        message="Your data has been successfully submitted.",
        duration=3000,
        )

        toast.show_toast()

        # Refresh table
        self.data.append((file_id, audit_id, file_name, file_status,file_importance, file_description, department_requested,requested_date))
        self.table.destroy()
        self.table = self.create_table()

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()

    
