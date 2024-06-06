import pandas as pd

# Read the Excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Chapter/allchap_Apr16_outputV2.xlsx')

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
df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Chapter/sec_allchap_Apr16_outputV3.xlsx', index=False)
