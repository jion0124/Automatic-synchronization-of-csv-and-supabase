import pandas as pd
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = 'https://xzplxylmqnrljazskyuq.supabase.co'
SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6cGx4eWxtcW5ybGphenNreXVxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc5MjE4NjUsImV4cCI6MjAzMzQ5Nzg2NX0.4CRHGN3oFeiFy7IQ4qxnRlTz_Q-qK1hBY337F_XQ9jY'

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Function to clear the Supabase table
def clear_table(table_name):
    try:
        response = supabase.table(table_name).delete().neq('企画番号', '').execute()
        if 'error' in response:
            print(f"Error truncating table: {response['error']}")
    except Exception as e:
        print(f"Error truncating table: {e}")

# Function to read CSV file and remove empty rows
def read_csv_and_clean(file_path):
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna(how='all')  # Remove rows where all elements are NaN
    return df_cleaned

# Function to update Supabase
def update_supabase(dataframe, table_name):
    for index, row in dataframe.iterrows():
        data = row.dropna().to_dict()  # Drop NaN values from the row
        print(f"Inserting row {index}: {data}")
        response = supabase.table(table_name).upsert(data, on_conflict=["企画番号"]).execute()
        if 'error' in response:
            print(f"Error inserting row {index}: {response['error']}")
        else:
            print(f"Successfully inserted row {index}")

# Main synchronization function
def synchronize_csv_to_supabase(file_path, table_name):
    # Clear Supabase table
    clear_table(table_name)
    
    # Read and clean CSV file
    dataframe = read_csv_and_clean(file_path)
    
    # Update Supabase
    update_supabase(dataframe, table_name)

# Path to your CSV file
csv_file_path = './実験.csv'
# Supabase table name
supabase_table_name = 'experiments'

# Run synchronization
synchronize_csv_to_supabase(csv_file_path, supabase_table_name)
