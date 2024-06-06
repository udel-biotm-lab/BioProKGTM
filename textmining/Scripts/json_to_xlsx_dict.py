import pandas as pd

# Path to your JSON file
json_file_path = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/transformed_data1.json"

# Load the JSON data into a DataFrame
df = pd.read_json(json_file_path, orient='index').reset_index()

# Rename the columns
df.columns = ['Terms', 'Type', 'COID']

# Save to Excel
output_excel_path = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/dict_terms.xlsx"
df.to_excel(output_excel_path, index=False)

print("Excel file has been created successfully at:", output_excel_path)
