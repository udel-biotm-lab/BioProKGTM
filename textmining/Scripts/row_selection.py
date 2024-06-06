import pandas as pd

# Load the Excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/outputV3.xlsx')

# Filter rows where either 'arg0_np' or 'arg1_np' is not empty
filtered_df = df[((df['arg0_matched'].notna() & df['arg1_matched'].isna()) | 
                  (df['arg0_matched'].isna() & df['arg1_matched'].notna()))]

# Write the filtered DataFrame to a new Excel file
filtered_df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/filtered_outputV3.xlsx', index=False)
