import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py <input_excel> <output_excel>")
    sys.exit(1)

input_excel = sys.argv[1]
output_excel = sys.argv[2]

# Read the Excel file
df = pd.read_excel(input_excel)

# Check if arg0_matched and arg1_matched have the same values in each row
mask = df['arg0_matched'] == df['arg1_matched']

# Drop rows where the values are the same in both columns
df = df[~mask]

# Save the updated DataFrame to a new Excel file
df.to_excel(output_excel, index=False)

print(f"Updated DataFrame saved to {output_excel}")
