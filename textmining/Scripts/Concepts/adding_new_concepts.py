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
    concepts = []
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            concept = {}
            for line in file:
                if line.startswith("[Term]"):
                    if concept:
                        concepts.append(concept)
                    concept = {"AlternativeNames": []}
                elif line.startswith("Id: "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) > 1:
                        concept["Id"] = parts[1]
                elif line.startswith("CanonicalName: "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) > 1:
                        concept["CanonicalName"] = parts[1]
                        existing_canonical_names.add(concept["CanonicalName"])
                elif line.startswith("TypeId: "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) > 1:
                        concept["TypeId"] = parts[1]
                elif line.startswith("Type: "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) > 1:
                        concept["Type"] = parts[1]
                elif line.startswith("AlternativeNames: "):
                    parts = line.strip().split(": ", 1)
                    if len(parts) > 1:
                        concept["AlternativeNames"].append(parts[1])
            if concept:
                concepts.append(concept)
    except FileNotFoundError:
        pass  # File does not exist yet, so we start fresh
    return concepts, existing_ids, existing_canonical_names

def write_concepts_to_file(output_file, concepts):
    """Write all concepts to the output file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for concept in concepts:
            file.write("[Term]\n")
            file.write(f"ConceptName: {concept['CanonicalName']}_{concept['Id']}\n")
            file.write(f"Id: {concept['Id']}\n")
            file.write(f"CanonicalName: {concept['CanonicalName']}\n")
            file.write(f"Type: {concept['Type']}\n")
            file.write(f"TypeId: {concept['TypeId']}\n")
            for alt_name in concept["AlternativeNames"]:
                file.write(f"AlternativeNames: {alt_name}\n")
            file.write("\n")

def add_term_to_concept_file(output_file, canonical_name, type_id, alternative_names, type_id_map, existing_ids):
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

def adjust_case(name):
    """Adjust the case of the name according to the rules specified."""
    if name.isupper():
        return name  # If all letters are capital, keep it as is
    else:
        return name.lower()  # Otherwise, convert to lowercase

def delete_concept(concepts, canonical_name, name_to_delete):
    """Delete a concept or specific alternative names from the list of concepts."""
    canonical_name = adjust_case(canonical_name)
    name_to_delete = adjust_case(name_to_delete)
    for concept in concepts:
        if concept["CanonicalName"] == canonical_name:
            if canonical_name == name_to_delete:
                concepts.remove(concept)
                return
            elif name_to_delete in concept["AlternativeNames"]:
                concept["AlternativeNames"].remove(name_to_delete)
                return

def update_concept(concepts, type_id_map):
    """Update a concept, its canonical name, alternative names, or TypeId."""
    canonical_name = adjust_case(input("Enter the CanonicalName to update: ").strip())
    for concept in concepts:
        if concept["CanonicalName"] == canonical_name:
            field_to_update = input("What would you like to update - CanonicalName (C), AlternativeNames (A), or TypeId (T)? ").strip().upper()
            
            if field_to_update == "C":
                print(f"Current CanonicalName: {concept['CanonicalName']}")
                new_name = adjust_case(input("Enter new CanonicalName (leave blank to keep current): ").strip())
                if new_name:
                    concept["CanonicalName"] = new_name
            
            elif field_to_update == "T":
                print(f"Current TypeId: {concept['TypeId']}")
                new_type_id = input("Enter new TypeId (leave blank to keep current): ").strip().upper()
                if new_type_id:
                    if not new_type_id.startswith('C') or not new_type_id[1:].isdigit() or new_type_id not in type_id_map:
                        print("Invalid TypeId. It must start with 'C' followed by numbers and must exist in the TypeId map.")
                    else:
                        concept["TypeId"] = new_type_id
                        concept["Type"] = type_id_map[new_type_id]
            
            elif field_to_update == "A":
                print(f"Current AlternativeNames: {', '.join(concept['AlternativeNames'])}")
                alt_action = input("Do you want to Add (A), Update (U), or Delete (D) an alternative name? ").strip().upper()
                
                if alt_action == "A":
                    while True:
                        alt_name = adjust_case(input("Enter new AlternativeName (leave blank to finish): ").strip())
                        if alt_name == "":
                            break
                        if alt_name != concept["CanonicalName"]:
                            concept["AlternativeNames"].append(alt_name)
                        else:
                            print("Alternative name is the same as the canonical name and will not be considered.")
                
                elif alt_action == "U":
                    current_alt_name = adjust_case(input("Enter the AlternativeName to update: ").strip())
                    if current_alt_name in concept["AlternativeNames"]:
                        new_alt_name = adjust_case(input("Enter new AlternativeName: ").strip())
                        if new_alt_name and new_alt_name != concept["CanonicalName"]:
                            concept["AlternativeNames"].remove(current_alt_name)
                            concept["AlternativeNames"].append(new_alt_name)
                        else:
                            print("Invalid new AlternativeName or same as CanonicalName.")
                    else:
                        print("AlternativeName not found.")
                
                elif alt_action == "D":
                    alt_name_to_delete = adjust_case(input("Enter the AlternativeName to delete: ").strip())
                    if alt_name_to_delete in concept["AlternativeNames"]:
                        concept["AlternativeNames"].remove(alt_name_to_delete)
                    else:
                        print("AlternativeName not found.")
                
                else:
                    print("Invalid choice.")
            else:
                print("Invalid choice. Please choose C, A, or T.")
            return

# Load TypeId to Type mapping
excel_file = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/type_type_id.xlsx'  # Update this path to your Excel file
type_id_map = load_type_ids_from_excel(excel_file)

# Define output file path
output_file = '/home/shovan/nlputils/EDG_framework/Waters_Deliverable/Concepts_and_Dictionary/concepts.obo' # Update this path to your OBO file

# Load existing concepts to check for uniqueness and to avoid duplicate IDs
concepts, existing_ids, existing_canonical_names = read_existing_concepts(output_file)

# Start of the interactive input process
while True:
    action = input("Choose an action - Add (A), Update (U), Delete (D), or Exit (E): ").strip().upper()
    if action == "E":
        break
    elif action == "A":
        canonical_name = adjust_case(input("CanonicalName: ").strip())

        # Check if the canonical name already exists
        if canonical_name in existing_canonical_names:
            print("A term with this CanonicalName already exists.")
            continue  # Skip the rest of the loop and ask for a new CanonicalName

        type_id = input("TypeId (must start with capital 'C'): ").strip().upper()
        # Validation for TypeId format and existence
        if not type_id.startswith('C') or not type_id[1:].isdigit() or type_id not in type_id_map:
            print("Invalid TypeId. It must start with 'C' followed by numbers and must exist in the TypeId map.")
            continue  # Prompt again for TypeId due to format error

        # Interactive section for inputting alternative names, with the new condition
        alternative_names = []
        add_alt_names = input("Do you want to add alternative names (Y/N)? ").strip().upper()
        if add_alt_names == "Y":
            while True:
                alt_name = adjust_case(input("AlternativeNames (leave blank and press enter if no more): ").strip())
                if alt_name == "":
                    break  # Exit the loop if the input is blank
                if alt_name != canonical_name:  # Check if alternative name is different from canonical name
                    alternative_names.append(alt_name)
                else:
                    print("Alternative name is the same as the canonical name and will not be considered.")

        # Add the term to the list of concepts
        concept_id, existing_ids = generate_concept_id(existing_ids=existing_ids)
        concept = {
            "Id": concept_id,
            "CanonicalName": canonical_name,
            "TypeId": type_id,
            "Type": type_id_map[type_id],
            "AlternativeNames": alternative_names
        }
        concepts.append(concept)
        existing_canonical_names.add(canonical_name)

    elif action == "U":
        update_concept(concepts, type_id_map)

    elif action == "D":
        canonical_name = adjust_case(input("Enter the CanonicalName for the entry to delete from: ").strip())
        name_to_delete = adjust_case(input("Enter the CanonicalName or AlternativeName to delete: ").strip())
        delete_concept(concepts, canonical_name, name_to_delete)
        if name_to_delete in existing_canonical_names:
            existing_canonical_names.remove(name_to_delete)

    else:
        print("Invalid action. Please choose A, U, D, or E.")

# Write updated concepts to the output file
write_concepts_to_file(output_file, concepts)
