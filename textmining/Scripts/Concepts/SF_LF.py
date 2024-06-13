import pandas as pd
import re
import sys

def extract_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    unique_pairs = set()
    pmid = ""
    for line in lines:
        # Check for PMID line
        if line.strip().endswith('.txt'):
            pmid = line.split('/')[-1].split('.')[0]
        
        # Check for data line
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                short_form, long_form, _ = parts[:3]
                pair = (short_form.strip(), long_form.strip())

                if pair not in unique_pairs:
                    unique_pairs.add(pair)
                    data.append({'PMID': pmid, 'Short Form': short_form.strip(), 'Long Form': long_form.strip()})

    return data

def write_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

if len(sys.argv) != 3:
    print("Usage: python script_name.py <input_file> <output_file>")
    sys.exit(1)

file_path = sys.argv[1]
output_file = sys.argv[2]

data = extract_data_from_file(file_path)
write_to_excel(data, output_file)
