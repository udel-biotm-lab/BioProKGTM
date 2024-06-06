import pandas as pd
import json

# Load the Excel file
excel_file_path = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/TP_OutputV1.xlsx'  # Update this path
df = pd.read_excel(excel_file_path)

# Load the JSON file
json_file_path = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/transformed_data.json'  # Update this path
with open(json_file_path) as json_file:
    data = json.load(json_file)

# The JSON structure is now a dict with the term as the key, and a list with type and concept id as values
dict_terms = data

# Initialize new columns
df['arg0_type'] = None
df['arg0_coid'] = None
df['arg1_type'] = None
df['arg1_coid'] = None

# Function to search and populate new columns
def populate_columns(row, dict_terms):
    arg0 = dict_terms.get(row['arg0_matched'])
    if arg0:
        row['arg0_type'], row['arg0_coid'] = arg0
    arg1 = dict_terms.get(row['arg1_matched'])
    if arg1:
        row['arg1_type'], row['arg1_coid'] = arg1
    return row

# Apply the function to each row
df = df.apply(lambda row: populate_columns(row, dict_terms), axis=1)

# Save the updated DataFrame to a new Excel file
output_file_path = 'updated_excel_file.xlsx'  # Update this path if needed
df.to_excel(output_file_path, index=False)
