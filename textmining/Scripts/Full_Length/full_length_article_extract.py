import xml.etree.ElementTree as ET
import os
import pandas as pd
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

# Function to ensure a text string ends with a period
def ensure_ending_period(text):
    if not text.endswith('.'):
        return text + '.'
    return text

# Function to preprocess text for known exceptions
def preprocess_text(text):
    # Handle known exceptions by replacing periods with a placeholder
    exceptions = {"et al.": "et al<PERIOD>", "Fig.": "Fig<PERIOD>"}
    for original, replacement in exceptions.items():
        text = text.replace(original, replacement)
    return text

# Function to postprocess text to revert placeholders back to periods
def postprocess_text(text):
    text = text.replace("<PERIOD>", ".")
    return text

# Initialize Punkt parameters
punkt_params = PunktParameters()
abbreviation_types = set(['fig', 'et al'])
punkt_params.abbrev_types = abbreviation_types

# Initialize Punkt tokenizer
tokenizer = PunktSentenceTokenizer(punkt_params)

# Function to split text into sentences using nltk's PunktSentenceTokenizer
def custom_sentence_splitter(text):
    # Preprocess to handle exceptions
    preprocessed_text = preprocess_text(text)
    
    # Tokenize text into sentences using nltk's tokenizer
    sentences = tokenizer.tokenize(preprocessed_text)
    
    # Postprocess sentences to revert any placeholders back to periods
    sentences = [postprocess_text(sentence.strip()) for sentence in sentences]
    
    # Ensure the last sentence ends with a period
    sentences[-1] = ensure_ending_period(sentences[-1])
    
    return sentences

def extract_passages_and_sentences_from_file(file_path):
    with open(file_path, 'r') as file:
        xml_data = file.read()

    root = ET.fromstring(xml_data)
    doc_id = root.find(".//document/id")
    doc_id = doc_id.text if doc_id is not None else "unknown"

    passages = []
    sentences_with_sections_and_docIds = []

    for passage in root.iter('passage'):
        section_type = passage.find("./infon[@key='section_type']")
        text = passage.find('text')

        if section_type is not None and text is not None:
            if section_type.text in ["TITLE", "ABSTRACT", "RESULTS"]:
                passage_text = text.text.strip()
                
                # Split passage text into sentences using the custom splitter
                sentences = custom_sentence_splitter(passage_text)
                for sentence in sentences:
                    sentences_with_sections_and_docIds.append((doc_id, sentence, section_type.text))

                passages.append(passage_text)

    return doc_id, passages, sentences_with_sections_and_docIds

# Initialize a DataFrame to store all sentences, sections, and docIds
df_sentences = pd.DataFrame(columns=["docId", "sentence", "section"])

# Set the directory path here
input_directory_path = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Full_Length_Article_XML"
output_directory_path1 = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Full_length"
output_directory_path2 = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Full_Length_Section"

# Iterate over each XML file in the directory
for filename in os.listdir(input_directory_path):
    if filename.endswith(".xml"):
        file_path = os.path.join(input_directory_path, filename)
        doc_id, extracted_passages, sentences_with_sections_and_docIds = extract_passages_and_sentences_from_file(file_path)

        # Convert the list of sentences, sections, and docIds to a DataFrame and append it to the main DataFrame
        df_temp = pd.DataFrame(sentences_with_sections_and_docIds, columns=["docId", "sentence", "section"])
        df_sentences = pd.concat([df_sentences, df_temp], ignore_index=True)

        # Write the extracted passages to a text file named after the document ID
        with open(f'{output_directory_path1}/{doc_id}.txt', 'w') as file:
            for passage in extracted_passages:
                passage_with_period = ensure_ending_period(passage)
                file.write(f"{passage_with_period}\n")

        print(f"Passages extracted and saved to '{doc_id}.txt'")            

# Finally, write the DataFrame to an Excel file
excel_path = os.path.join(output_directory_path2, 'extracted_sentences_sections_docIds.xlsx')
df_sentences.to_excel(excel_path, index=False)

print(f"All sentences, sections, and document IDs have been saved to '{excel_path}'.")
