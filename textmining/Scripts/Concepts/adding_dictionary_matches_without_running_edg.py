import pandas as pd
import json
import re

# Load the Excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/abs_more_Apr19_outputV1.xlsx')

# Load the JSON file
with open('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/transformed_data1.json') as json_file:
    data = json.load(json_file)

def match_terms(arg, dictionary):
    if not isinstance(arg, str):
        arg = str(arg)

    matches = []

    # Collect all potential matches from the dictionary
    for term, entry in dictionary.items():
        # Adjust pattern for case sensitivity
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', flags=(0 if term.isupper() else re.IGNORECASE))
        for match in pattern.finditer(arg):
            exact_match = arg[match.start():match.end()]
            matches.append((exact_match, entry[0], entry[1]))  # Store matches as (term, type, coid)

    # Ensure no shorter match that is contained within a longer match
    filtered_matches = []
    for current_match in matches:
        if not any(current_match[0].lower() in other_match[0].lower() for other_match in matches if other_match != current_match):
            filtered_matches.append(current_match)

    # Sort matches by length in descending order to prioritize longer matches
    filtered_matches.sort(key=lambda x: len(x[0]), reverse=True)

    # Extract and return the match information
    matched_terms, matched_types, matched_coids = zip(*filtered_matches) if filtered_matches else ([], [], [])
    return matched_terms, matched_types, matched_coids


def populate_columns(row, dictionary):
    matched_terms, matched_types, matched_coids = match_terms(row['arg0_np'], dictionary)
    if matched_terms:
        row['arg0_matched'] = ', '.join(matched_terms)
        row['arg0_type'] = ', '.join(matched_types)
        row['arg0_coid'] = ', '.join(matched_coids)

    matched_terms, matched_types, matched_coids = match_terms(row['arg1_np'], dictionary)
    if matched_terms:
        row['arg1_matched'] = ', '.join(matched_terms)
        row['arg1_type'] = ', '.join(matched_types)
        row['arg1_coid'] = ', '.join(matched_coids)

    return row

# Apply the function to each row in the dataframe
df = df.apply(lambda row: populate_columns(row, data), axis=1)

# Save the updated dataframe to an Excel file
df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/abs_more_Apr19_outputV2.xlsx', index=False)
