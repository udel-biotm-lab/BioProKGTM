import pandas as pd
import json

file_path = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/dict_hierV6.xlsx'
df = pd.read_excel(file_path)

term_to_hierarchy = {}

for index, row in df.iterrows():
    current_class = row['Class']
    current_subclass = row['Subclass']
    sub_subclass = row['Subsubclass']
    terms = row['Terms'].split(', ')

    terms = [term.strip() for term in terms]

    for term in terms:
        hierarchy = []

        if sub_subclass and not pd.isnull(sub_subclass):
            hierarchy.append(str(sub_subclass))
        elif current_subclass and not pd.isnull(current_subclass):
            hierarchy.append(str(current_subclass))
        elif current_class and not pd.isnull(current_class):
            hierarchy.append(str(current_class))

        # Ensure hierarchy is always a list, even if it's a single class
        term_to_hierarchy[term] = [h.encode('utf-8').decode('utf-8') for h in hierarchy] if hierarchy else []

# Separate terms into uppercase and lowercase groups
uppercase_terms = [term for term in term_to_hierarchy.keys() if term.isupper()]
lowercase_terms = [term for term in term_to_hierarchy.keys() if not term.isupper()]

# Sort each group alphabetically
sorted_uppercase_terms = sorted(uppercase_terms)
sorted_lowercase_terms = sorted(lowercase_terms)

# Combine the sorted groups
sorted_terms = sorted_uppercase_terms + sorted_lowercase_terms

sorted_term_to_hierarchy = {}
for term in sorted_terms:
    sorted_term_to_hierarchy[term] = term_to_hierarchy[term]

with open('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/output.txt', 'w', encoding='utf-8') as file:
    json.dump(sorted_term_to_hierarchy, file, ensure_ascii=False, indent=4)
