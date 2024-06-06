import json

# Function to find dissimilar items between two dictionaries
def find_dissimilar_items(dict1, dict2):
    dissimilar_items = {
        'unique_to_dict1': [],
        'unique_to_dict2': []
    }

    # Check what's unique to dict1
    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            dissimilar_items['unique_to_dict1'].append({key: value})

    # Check what's unique to dict2
    for key, value in dict2.items():
        if key not in dict1 or dict1[key] != value:
            dissimilar_items['unique_to_dict2'].append({key: value})

    return dissimilar_items

# Load JSON files
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Specify the paths to your two JSON files
json_file_path1 = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/transformed_data.json'  # Replace with the actual file path
json_file_path2 = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/transformed_data1.json'  # Replace with the actual file path

# Load the content of the JSON files into dictionaries
dict1 = load_json_file(json_file_path1)
dict2 = load_json_file(json_file_path2)

# Finding dissimilar items
dissimilar_items = find_dissimilar_items(dict1, dict2)
print(json.dumps(dissimilar_items, indent=2))
