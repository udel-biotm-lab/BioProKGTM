import json
import sys

def parse_obo(file_path):
    with open(file_path, 'r') as file:
        obo_content = file.read()

    terms = obo_content.strip().split("[Term]")
    parsed_data = {}
    for term in terms[1:]:  # Skip the first split part as it's the header
        lines = term.strip().split("\n")
        term_data = {}
        alternative_names = []
        
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                if key == "AlternativeNames":
                    alternative_names.append(value)
                else:
                    term_data[key] = value
        
        canonical_name = term_data.get("CanonicalName")
        type_id = term_data.get("Type")
        coid = term_data.get("Id")
        
        # Mapping for CanonicalName and AlternativeNames
        if canonical_name:
            parsed_data[canonical_name] = [type_id, coid]
            for alt_name in alternative_names:
                if alt_name:  # Ensure it's not empty
                    parsed_data[alt_name] = [type_id, coid]
                
    return parsed_data

def save_transformed_data_to_json_file(transformed_data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(transformed_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Parse the OBO content
    transformed_data = parse_obo(input_file)
    
    # Save the transformed data to a JSON file
    save_transformed_data_to_json_file(transformed_data, output_file)
    
    print(f"Transformed data has been saved to {output_file} in JSON format.")
