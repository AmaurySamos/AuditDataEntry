import os
from google.cloud import bigquery
import pandas as pd
from datetime import datetime

# Replace with the correct full path to your JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\arsamos\\OneDrive - Belize Telemedia Ltd\\Desktop\\Audits Data Entry\\audit-447319-0fddfcde1756.json"

# Set up your BigQuery client
client = bigquery.Client(project = "audit-447319")

# Define the dataset ID (in the format project_id.dataset_id)
dataset_id = f"{client.project}.Audits"

# Create a DatasetReference
dataset = bigquery.Dataset(dataset_id)

# Optional: Set dataset properties (like description)
dataset.description = "This dataset contains audit-related tables."

# Create the dataset
try:
    dataset = client.create_dataset(dataset, timeout=30)  # API request
    print(f"Dataset {dataset_id} created successfully.")
except Exception as e:
    print(f"Failed to create dataset: {e}")
    
# Define your project, dataset, and table
project_id = "audit-447319"
dataset_id = "Audits"

table_id = "Audit_Program"
table_id1 = "Auditor"
table_id2 = "Division"

# Define the table schema
schema = [
    bigquery.SchemaField("audit_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("auditor_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("request_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("audit_project", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("epic", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("userstory", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("owner", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("department", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("division_id", "INTEGER", mode="REQUIRED"), 
    bigquery.SchemaField("fy_quarter", "INTEGER", mode="REQUIRED"), 
    bigquery.SchemaField("sprint_cycle", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("status_of_audit", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("audit_start_date", "DATE", mode="REQUIRED"), 
    bigquery.SchemaField("date_for_deliverable", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("actual_date_delivered", "DATE", mode="REQUIRED"),     
]

schema1 = [
    bigquery.SchemaField("auditor_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("auditor_name", "STRING", mode="REQUIRED"),  
]

schema2 = [
    bigquery.SchemaField("division_id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("division_name", "STRING", mode="REQUIRED"),  
    bigquery.SchemaField("department", "STRING", mode="REQUIRED"),  
]

# Construct the table reference
table_ref = f"{project_id}.{dataset_id}.{table_id}"
table_ref1 = f"{project_id}.{dataset_id}.{table_id1}"
table_ref2 = f"{project_id}.{dataset_id}.{table_id2}"

# Define the table
table = bigquery.Table(table_ref, schema=schema)
table1 = bigquery.Table(table_ref1, schema=schema1)
table2 = bigquery.Table(table_ref2, schema=schema2)

# Create the table in BigQuery
try:
    created_table = client.create_table(table)
    created_table1 = client.create_table(table1)
    created_table2 = client.create_table(table2)
    print(f"Table {created_table.full_table_id} created successfully.")
    print(f"Table {created_table1.full_table_id1} created successfully.")
    print(f"Table {created_table2.full_table_id2} created successfully.")
except Exception as e:
    print(f"Error: {e}")
    
# # Create a DataFrame
# df = pd.DataFrame([
#     {
#         "audit_id": "AUD001",
#         "auditor_id": 1,
#         "request_id": 1,
#         "audit_project": "Prepaid Mobile Audit",
#         "epic": "Revenue Assurance",
#         "userstory": "US1234",
#         "owner": "John Doe",
#         "department": "Finance",
#         "division_id": 1,
#         "fy_quarter": 1,
#         "sprint_cycle": 1,
#         "status_of_audit": "In Progress",
#         "audit_start_date": "2025-01-01",
#         "date_for_deliverable": "2025-03-01",
#         "actual_date_delivered": "2025-02-28",
#     }
# ])

# # 🛠 Convert columns to datetime
# df["audit_start_date"] = pd.to_datetime(df["audit_start_date"]).dt.date
# df["date_for_deliverable"] = pd.to_datetime(df["date_for_deliverable"]).dt.date
# df["actual_date_delivered"] = pd.to_datetime(df["actual_date_delivered"]).dt.date

# # Define table path
# table_path = f"{project_id}.{dataset_id}.{table_id}"

# # Load to BigQuery
# job = client.load_table_from_dataframe(df, table_path)
# job.result()  # Wait for the job to complete
# print("Row inserted successfully via batch load.")

# # Auditor table
# auditors_df = pd.DataFrame([
#     {"auditor_id": 1, "auditor_name": "Lupita Blanco"},
#     {"auditor_id": 2, "auditor_name": "Annel Lemus"},
# ])

# client.load_table_from_dataframe(auditors_df, f"{project_id}.{dataset_id}.{table_id1}").result()
# print("Auditor data inserted.")

# # Division table
# divisions_df = pd.DataFrame([
#     {"division_id": 1, "division_name": "Network Ops", "department": "Engineering"},
#     {"division_id": 2, "division_name": "Customer Service", "department": "Support"},
# ])

# client.load_table_from_dataframe(divisions_df, f"{project_id}.{dataset_id}.{table_id2}").result()
# print("Division data inserted.")