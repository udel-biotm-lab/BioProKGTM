import pandas as pd
from itertools import product

def preprocess_step_zero(row):
    """Preprocess arg_matched based on arg_base and arg_head."""
    for arg_side in ['arg0', 'arg1']:
        matched_terms = str(row[f'{arg_side}_matched']).split(', ')
        types = str(row[f'{arg_side}_type']).split(', ')
        coids = str(row[f'{arg_side}_coid']).split(', ')
        arg_base = str(row[f'{arg_side}_base']).lower()
        arg_head = str(row[f'{arg_side}_head']).lower()

        # Check if arg_matched is in arg_base
        matches_in_base = [i for i, term in enumerate(matched_terms) if term.lower() in arg_base]

        if matches_in_base:
            # Keep matches in arg_base
            keep_indices = matches_in_base
        else:
            # If not in arg_base, check arg_head
            matches_in_head = [i for i, term in enumerate(matched_terms) if term.lower() in arg_head]
            if matches_in_head:
                # Keep matches in arg_head
                keep_indices = matches_in_head
            else:
                # If not in arg_head, keep all
                keep_indices = range(len(matched_terms))

        # Update the row based on keep_indices
        row[f'{arg_side}_matched'] = ', '.join([matched_terms[i] for i in keep_indices])
        row[f'{arg_side}_type'] = ', '.join([types[i] for i in keep_indices])
        row[f'{arg_side}_coid'] = ', '.join([coids[i] for i in keep_indices])

    return row

def preprocess_and_refine_matches(row):
    """Refine matches according to specified rules involving 'of', 'by', 'through', 'with', and 'in'."""
    for arg_side in ['arg0', 'arg1']:
        np_phrase = str(row[f'{arg_side}_np']).lower()
        matched_terms = str(row[f'{arg_side}_matched']).split(', ')
        types = str(row[f'{arg_side}_type']).split(', ')
        coids = str(row[f'{arg_side}_coid']).split(', ')

        # Initialize positions
        start_pos = 0
        end_pos = len(np_phrase)

        # Find positions of 'of', 'by', 'through', 'with', and 'in'
        of_indices = [i for i in range(len(np_phrase)) if np_phrase.startswith(' of ', i)]
        by_index = np_phrase.find(' by ')
        through_index = np_phrase.find(' through ')
        with_index = np_phrase.find(' with ')
        in_index = np_phrase.find(' in ')

        # Handling "with" as a special case if it's the only preposition
        if with_index != -1 and all(idx == -1 for idx in [by_index, through_index, of_indices, in_index]):
            start_pos = with_index + 5  # Start after "with"

        # Determine the first occurrence of "by", "through", or "in" considering the new rule for "in"
        by_through_in_indices = [idx for idx in [by_index, through_index, in_index] if idx != -1]
        first_by_through_in_index = min(by_through_in_indices) if by_through_in_indices else len(np_phrase)

        # Apply rules for "of" and the updated rule for "by/through/in"
        if of_indices:
            start_pos = max(start_pos, of_indices[0] + 4)  # Ensure "with" rule is respected
            if len(of_indices) >= 2:  # Multiple "of"
                end_pos = of_indices[-1]  # End at the last "of"
            # No else needed; for a single "of", the start_pos adjustment is enough

        # Apply the updated rule for "by/through/in"
        if first_by_through_in_index < end_pos:
            end_pos = min(end_pos, first_by_through_in_index)

        refined_matches = []
        for term, type_, coid in zip(matched_terms, types, coids):
            term_pos = np_phrase.find(term.lower())
            if start_pos <= term_pos < end_pos:
                refined_matches.append((term, type_, coid))

        # Clear existing matches if no refinement criteria met
        if not refined_matches:
            row[f'{arg_side}_matched'], row[f'{arg_side}_type'], row[f'{arg_side}_coid'] = '', '', ''
        else:
            # Update the row with refined matches, types, and coids
            matches, types, coids = zip(*refined_matches)  # Unzip the refined matches
            row[f'{arg_side}_matched'] = ', '.join(matches)
            row[f'{arg_side}_type'] = ', '.join(types)
            row[f'{arg_side}_coid'] = ', '.join(coids)

    return row






def split_matches(types_str, coids_str):
    """Split types and coids strings into lists."""
    types = types_str.split(', ')
    coids = coids_str.split(', ')
    return types, coids

def generate_combinations(row):
    """Generate all combinations of arg0 and arg1 matches, excluding rows where matches are 'nan'."""
    # Convert to string and split; ensures handling NaN or numeric values correctly
    arg0_matches = str(row['arg0_matched']).split(', ')
    arg1_matches = str(row['arg1_matched']).split(', ')
    arg0_types, arg0_coids = split_matches(str(row['arg0_type']), str(row['arg0_coid']))
    arg1_types, arg1_coids = split_matches(str(row['arg1_type']), str(row['arg1_coid']))

    combinations = []
    for i, arg0_match in enumerate(arg0_matches):
        for j, arg1_match in enumerate(arg1_matches):
            # Check if either match is 'nan' and skip if so
            if arg0_match.strip().lower() == 'nan' or arg1_match.strip().lower() == 'nan':
                continue

            new_row = row.copy()
            new_row['arg0_matched'] = arg0_match.strip()
            new_row['arg1_matched'] = arg1_match.strip()

            # Assign type and coid if they exist and are not 'nan'
            if i < len(arg0_types) and arg0_types[i].strip().lower() != 'nan':
                new_row['arg0_type'] = arg0_types[i].strip()
            if i < len(arg0_coids) and arg0_coids[i].strip().lower() != 'nan':
                new_row['arg0_coid'] = arg0_coids[i].strip()
            if j < len(arg1_types) and arg1_types[j].strip().lower() != 'nan':
                new_row['arg1_type'] = arg1_types[j].strip()
            if j < len(arg1_coids) and arg1_coids[j].strip().lower() != 'nan':
                new_row['arg1_coid'] = arg1_coids[j].strip()

            combinations.append(new_row)
    return combinations


def filter_rows_based_on_criteria(rows):
    """Filter out rows based on specified criteria."""
    filtered_rows = []
    for row in rows:
        # Normalize values for comparison
        arg0_np = str(row['arg0_np']).strip().lower()
        arg1_np = str(row['arg1_np']).strip().lower()
        arg0_matched = str(row['arg0_matched']).strip().lower()
        arg1_matched = str(row['arg1_matched']).strip().lower()

        # Condition 1: Remove if arg0_np and arg1_np are the same
        if arg0_np == arg1_np:
            continue  # Skip this row
        
        # Condition 2: If arg0_np and arg1_np are different, remove if arg0_matched and arg1_matched are the same
        if arg0_matched == arg1_matched:
            continue  # Skip this row

        # If neither condition is met, include the row
        filtered_rows.append(row)
    
    return filtered_rows

def filter_empty_matches(rows):
    """Filter out rows where either arg0_matched or arg1_matched (or both) are empty."""
    filtered_rows = []
    for row in rows:
        arg0_matched = str(row['arg0_matched']).strip().lower()
        arg1_matched = str(row['arg1_matched']).strip().lower()

        # Discard the row if either arg0_matched or arg1_matched (or both) are empty
        if not arg0_matched or not arg1_matched:
            continue

        filtered_rows.append(row)
    return filtered_rows




def process_excel(input_excel, output_excel):
    """Load the Excel file, process each row to create multiple rows for each combination of matches, and save the updated DataFrame."""
    df = pd.read_excel(input_excel)
    
    # Split the DataFrame into two parts: one for rows with single matches and one for rows with multiple matches
    single_match_df = df[(df['arg0_matched'].str.count(',') < 1) & (df['arg1_matched'].str.count(',') < 1)]
    multiple_matches_df = df[~((df['arg0_matched'].str.count(',') < 1) & (df['arg1_matched'].str.count(',') < 1))]

    # Only apply preprocessing and refining steps to rows with multiple matches
    preprocessed_df = multiple_matches_df.apply(preprocess_step_zero, axis=1)
    refined_df = preprocessed_df.apply(preprocess_and_refine_matches, axis=1)

    # Step 2: Generate combinations of arg0 and arg1 matches
    new_rows_list = refined_df.apply(generate_combinations, axis=1).tolist()
    flat_list = [item for sublist in new_rows_list for item in sublist]

    # Step 3 and Step 4: Filter rows based on new criteria and for empty matches
    filtered_list = filter_rows_based_on_criteria(flat_list)
    filtered_list = filter_empty_matches(filtered_list)

    # Combine single_match_df with the filtered and processed multiple matches
    combined_df = pd.concat([pd.DataFrame(filtered_list), single_match_df], ignore_index=True)

    # Step 5: Drop duplicate rows based on certain columns
    final_df = combined_df.drop_duplicates(subset=['trigger', 'arg0_np', 'arg0_matched', 'arg1_np', 'arg1_matched', 'sent_text'])

    final_df.to_excel(output_excel, index=False)



if __name__ == '__main__':
    input_excel = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/abs_more_Apr19_outputV2.xlsx"
    output_excel = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/abs_more_Apr19_outputV3.xlsx"

    process_excel(input_excel, output_excel)
