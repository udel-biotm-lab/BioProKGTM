import pandas as pd
import string

# Function to normalize text for comparison purposes
def normalize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove leading and trailing whitespaces
    text = text.strip()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Load the input sentences Excel file
input_df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/rel_Apr14_outputV2.xlsx')  # Adjust the path as needed

# Load the sentences with sections and docIds Excel file
sections_df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Full_Length_Section/extracted_sentences_sections_docIds.xlsx')  # Adjust the path as needed

# Normalize sentences in both DataFrames for comparison
input_df['normalized_sent_text'] = input_df['sent_text'].astype(str).apply(normalize_text)
sections_df['normalized_sentence'] = sections_df['sentence'].apply(normalize_text)

# Create a dictionary from sections_df for faster lookup using normalized sentences
sections_dict = pd.Series(sections_df['section'].values, index=sections_df['normalized_sentence']).to_dict()

# Define a function to get section from the dictionary
def get_section(normalized_sent_text):
    return sections_dict.get(normalized_sent_text, None)  # Returns None if the sentence is not found

# Apply the function to the 'normalized_sent_text' column to create a new 'Section' column
input_df['Section'] = input_df['normalized_sent_text'].apply(get_section)

# Drop the temporary 'normalized_sent_text' column as it's no longer needed
input_df.drop('normalized_sent_text', axis=1, inplace=True)

# Save the updated DataFrame to a new Excel file
output_excel_path = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Full_Length/sec_rel_Apr14_outputV2.xlsx'  # Adjust the path as needed
input_df.to_excel(output_excel_path, index=False)

print(f"Updated input sentences with sections have been saved to '{output_excel_path}'.")
