import pandas as pd

# Read the Excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/sec_rel_Apr14_outputV2.xlsx')

# Check if arg0_matched and arg1_matched have the same values in each row
mask = df['arg0_matched'] == df['arg1_matched']

# Drop rows where the values are the same in both columns
df = df[~mask]

# Save the updated DataFrame to a new Excel file
df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/sec_rel_Apr19_outputV2.xlsx', index=False)
