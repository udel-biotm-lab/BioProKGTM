import json
import random
import pandas as pd  # Make sure pandas is imported

def generate_concept_id(prefix="COID", length=6, existing_ids=None):
    """Generate a unique random concept ID."""
    if existing_ids is None:
        existing_ids = set()
    while True:
        number = ''.join(random.choices('0123456789', k=length))
        concept_id = f"{prefix}{number}"
        if concept_id not in existing_ids:
            existing_ids.add(concept_id)
            return concept_id

def load_type_ids_from_excel(excel_file):
    """Load Type and TypeId mappings from an Excel file."""
    df = pd.read_excel(excel_file, engine='openpyxl')  # Make sure to specify the path to your Excel file
    type_id_map = df.set_index('Type')['TypeId'].to_dict()
    return type_id_map

def create_concept_obo_file(input_file, output_file, type_id_map):
    existing_ids = set()  # Keep track of generated IDs to ensure uniqueness
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            terms_data = json.load(file)
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to load JSON: {e}")
        return  # Stop execution if JSON is invalid

    with open(output_file, 'w', encoding='utf-8') as file:
        # Write the header for the OBO file
        file.write("format-version: 1.0\n")
        file.write("date: 2024-02-21\n")
        file.write("auto-generated-by: Shovan\n\n")

        for term, type_info in terms_data.items():
            concept_id = generate_concept_id(existing_ids=existing_ids)  # Ensure unique ID
            type_id = type_id_map.get(type_info[0], "")  # Lookup TypeId using the Type
            file.write("[Term]\n")
            file.write(f"ConceptName: {term}_{concept_id}\n")
            file.write(f"Id: {concept_id}\n")
            file.write(f"CanonicalName: {term}\n")
            file.write(f"Type: {type_info[0]}\n")
            file.write(f"TypeId: {type_id}\n")
            file.write("AlternativeNames: \n\n")

# Example usage
excel_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/type_type_id.xlsx'  # Update this path to your Excel file
type_id_map = load_type_ids_from_excel(excel_file)

input_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/output.txt'
output_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/concepts.obo'
create_concept_obo_file(input_file, output_file, type_id_map)
