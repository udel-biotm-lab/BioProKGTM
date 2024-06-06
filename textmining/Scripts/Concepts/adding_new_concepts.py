import json
import random
import pandas as pd

def generate_concept_id(prefix="COID", length=6, existing_ids=None):
    """Generate a unique random concept ID."""
    if existing_ids is None:
        existing_ids = set()
    while True:
        number = ''.join(random.choices('0123456789', k=length))
        concept_id = f"{prefix}{number}"
        if concept_id not in existing_ids:
            existing_ids.add(concept_id)
            return concept_id, existing_ids
    return None, existing_ids  # In case of an unlikely failure to generate a new ID

def load_type_ids_from_excel(excel_file):
    """Load Type and TypeId mappings from an Excel file."""
    df = pd.read_excel(excel_file, engine='openpyxl')
    type_id_map = df.set_index('TypeId')['Type'].to_dict()  # Inverting to map from TypeId to Type
    return type_id_map

def read_existing_concepts(output_file):
    """Read existing concepts from an OBO file to extract existing IDs and canonical names."""
    existing_ids = set()
    existing_canonical_names = set()
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('Id: COID'):
                    existing_ids.add(line.strip().split(': ')[1])
                elif line.startswith('CanonicalName: '):
                    existing_canonical_names.add(line.strip().split(': ')[1])
    except FileNotFoundError:
        pass  # File does not exist yet, so we start fresh
    return existing_ids, existing_canonical_names

def add_term_to_concept_file(output_file, canonical_name, type_id, alternative_names, type_id_map, existing_ids, existing_canonical_names):
    concept_id, existing_ids = generate_concept_id(existing_ids=existing_ids)
    type_name = type_id_map.get(type_id, "")
    if not type_name:
        print(f"No Type found for TypeId: {type_id}")
        return
    
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write("[Term]\n")
        file.write(f"ConceptName: {canonical_name}_{concept_id}\n")
        file.write(f"Id: {concept_id}\n")
        file.write(f"CanonicalName: {canonical_name}\n")
        file.write(f"Type: {type_name}\n")
        file.write(f"TypeId: {type_id}\n")
        # Writing alternative names
        if alternative_names:  # Check if there are any alternative names provided
            for alt_name in alternative_names:
                file.write(f"AlternativeNames: {alt_name}\n")
        else:
            # If no alternative names, still include the field but leave it blank
            file.write("AlternativeNames: \n")

        file.write("\n")

# Load TypeId to Type mapping
excel_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/type_type_id.xlsx'  # Update this path to your Excel file
type_id_map = load_type_ids_from_excel(excel_file)

# Define output file path
output_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/conceptsV2.obo'

# Load existing concepts to check for uniqueness and to avoid duplicate IDs
existing_ids, existing_canonical_names = read_existing_concepts(output_file)

# Start of the interactive input process
while True:
    canonical_name = input("CanonicalName: ").strip()
    # Check if the canonical name already exists
    if canonical_name in existing_canonical_names:
        print("A term with this CanonicalName already exists.")
        continue  # Skip the rest of the loop and ask for a new CanonicalName

    type_id = input("TypeId (must start with capital 'C'): ").strip()
    # Validation for TypeId format and existence
    if not type_id.startswith('C') or not type_id[1:].isdigit():
        print("Invalid TypeId. It must start with 'C' followed by numbers.")
        continue  # Prompt again for TypeId due to format error

    # Check if the TypeId exists in the mapping
    if type_id not in type_id_map:
        print(f"No Type found for TypeId: {type_id}")
        continue  # Prompt again for inputs starting from CanonicalName

    # Interactive section for inputting alternative names, with the new condition
    alternative_names = []
    add_alt_names = input("Do you want to add alternative names (Y/N)? ").strip().upper()
    if add_alt_names == "Y":
        while True:
            alt_name = input("AlternativeNames (leave blank and press enter if no more): ").strip()
            if alt_name == "":
                break  # Exit the loop if the input is blank
            if alt_name != canonical_name:  # Check if alternative name is different from canonical name
                alternative_names.append(alt_name)
            else:
                print("Alternative name is the same as the canonical name and will not be considered.")


    # The rest of the logic to add the term to the concept file remains unchanged
    add_term_to_concept_file(output_file, canonical_name, type_id, alternative_names, type_id_map, existing_ids, existing_canonical_names)
    existing_canonical_names.add(canonical_name)  # Update the set of existing canonical names

    add_another = input("Add another term (Y/N)? ").strip().upper()
    if add_another != "Y":
        break

