import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py <input_excel> <output_excel>")
    sys.exit(1)

input_excel = sys.argv[1]
output_excel = sys.argv[2]

# Read the Excel file
df = pd.read_excel(input_excel)

# Function to extract chapter number from PMID
def extract_chapter(pmid):
    parts = pmid.split('_')
    for part in parts:
        if part.isdigit():
            return f'CHAPTER {part}'
    return None

# Apply the function to the PMID column to create the section column
df['section'] = df['PMID'].apply(extract_chapter)

# Print the updated DataFrame
#print(df)

# Save the updated DataFrame to a new Excel file
df.to_excel(output_excel, index=False)

print(f"Updated DataFrame with sections saved to '{output_excel}'.")
