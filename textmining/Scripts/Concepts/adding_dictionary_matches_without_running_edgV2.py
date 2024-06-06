import pandas as pd
import json
import re
import inflect

# Load the Excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/TP_OutputV3.xlsx')

# Load the JSON file
with open('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Concepts_and_Dictionary/transformed_data1.json') as json_file:
    data = json.load(json_file)

    
# Initialize inflect engine
p = inflect.engine()

def normalize_term(term):
    # Replace hyphens with spaces and convert to lowercase for consistent matching
    return re.sub(r'[-]', ' ', term).lower()

def is_plural(word):
    # Check if a word is plural; this is a simplification and works for most English words
    return p.singular_noun(word) is not False


def match_terms(arg, dictionary):
    matched_terms = []
    matched_types = []
    matched_coids = []
    exact_matches = []

    if not isinstance(arg, str):
        arg = str(arg)

    normalized_arg = normalize_term(arg)  # Normalize the input argument

    # Attempt to find an exact match first
    for term in dictionary.keys():
        pattern = re.compile(re.escape(term), re.IGNORECASE)  # Use the term to create a regex pattern
        if pattern.search(arg):  # Check for matches using the pattern
            entry = dictionary[term]
            for match in pattern.finditer(arg):
                exact_match = arg[match.start():match.end()]  # Extract the exact match from arg
                if exact_match not in exact_matches:  # Avoid duplicate entries
                    matched_terms.append(exact_match)  # Append the exact substring that was matched
                    matched_types.append(entry[0])
                    matched_coids.append(entry[1])
                    exact_matches.append(exact_match)  # Keep track of exact matches to avoid duplicates
                    print(f"Exact match found: {exact_match}")
            return matched_terms, matched_types, matched_coids  # Return immediately after finding an exact match

    # If no exact match, proceed with the previous logic
    sorted_terms = sorted(dictionary.keys(), key=len, reverse=True)

    for term in sorted_terms:
        entry = dictionary[term]
        normalized_term = normalize_term(term)  # Normalize dictionary term
        pattern = re.compile(re.escape(normalized_term), re.IGNORECASE)

        for match in pattern.finditer(normalized_arg):
            exact_match = arg[match.start():match.end()]  # Extract the exact match from arg
            if exact_match not in exact_matches:  # Avoid duplicates
                matched_terms.append(exact_match)  # Append the exact substring that was matched
                matched_types.append(entry[0])
                matched_coids.append(entry[1])
                exact_matches.append(exact_match)  # Keep track of exact matches to avoid duplicates
                print(f"Match found: {exact_match}")

    return matched_terms, matched_types, matched_coids



def populate_columns(row, dictionary):
    # Process arg0_np
    matched_terms, matched_types, matched_coids = match_terms(row['arg0_np'], dictionary)
    if matched_terms:
        row['arg0_matched'] = ', '.join(matched_terms)
        row['arg0_type'] = ', '.join(matched_types)
        row['arg0_coid'] = ', '.join(matched_coids)

    # Process arg1_np
    matched_terms, matched_types, matched_coids = match_terms(row['arg1_np'], dictionary)
    if matched_terms:
        row['arg1_matched'] = ', '.join(matched_terms)
        row['arg1_type'] = ', '.join(matched_types)
        row['arg1_coid'] = ', '.join(matched_coids)

    return row

df = df.apply(lambda row: populate_columns(row, data), axis=1)

df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/updated_TP_OutputV3.xlsx', index=False)
