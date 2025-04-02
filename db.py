import os
from google.cloud import bigquery

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

# table_id = "Audit"
# table_id1 = "Auditor"

# # Define the table schema
# schema = [
#     bigquery.SchemaField("audit_id", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_name", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_start_date", "DATE", mode="REQUIRED"),
#     bigquery.SchemaField("audit_end_date", "DATE", mode="REQUIRED"),
#     bigquery.SchemaField("auditor_id", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_description", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_importance_level", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_status", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("audit_actual_end_date", "DATE", mode="REQUIRED"),    
# ]

# schema1 = [
#     bigquery.SchemaField("auditor_id", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("auditor_name", "STRING", mode="REQUIRED"),  
# ]

# # Construct the table reference
# table_ref = f"{project_id}.{dataset_id}.{table_id}"
# table_ref1 = f"{project_id}.{dataset_id}.{table_id1}"

# # Define the table
# table = bigquery.Table(table_ref, schema=schema)
# table1 = bigquery.Table(table_ref1, schema=schema1)

# # Create the table in BigQuery
# try:
#     created_table = client.create_table(table)
#     created_table1 = client.create_table(table1)
#     print(f"Table {created_table.full_table_id} created successfully.")
#     print(f"Table {created_table1.full_table_id1} created successfully.")
# except Exception as e:
#     print(f"Error: {e}")