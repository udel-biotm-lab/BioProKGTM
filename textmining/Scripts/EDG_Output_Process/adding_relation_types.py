import pandas as pd
import re

# Load the excel file
df = pd.read_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/abs_more_Apr19_outputV3.xlsx')  # Adjust path accordingly

# Define keyword patterns
INCREASE_KEYWORDS = [r'\bincreas\w*\b', r'\benhanc\w*\b', r'\bris\w*\b', r'\belevat\w*\b', r'\bhigh\b', r'\bhigh\B', r'\bhigher\w*\b', r'\bhighest\b', r'\bmore\b', r'\bupregul\w*\b', r'\bup\b', r'\badd\w*\b']
DECREASE_KEYWORDS = [r'\bdecreas\w*\b', r'\breduc\w*\b', r'\bfall\w*\b', r'\bdrop\w*\b', r'\bdiminish\w*\b', r'(?<!\S)low\w*\b', r'\bless\b', r'\bdownregul\w*\b', r'\bdown\b', r'\binhibit(?!or(s)?\b)\w*\b']
NEGATION_TERMS = [r'\bno\b', r'\bnot\b', r'\bn\'t\b', r'\bnever\b']

# Convert keyword lists to patterns
increase_pattern = "|".join(INCREASE_KEYWORDS)
decrease_pattern = "|".join(DECREASE_KEYWORDS)
negation_pattern = "|".join(NEGATION_TERMS)

def has_negation_before_trigger(text, trigger):
    # Create a pattern to search for negation terms followed by the trigger
    pattern = r'(' + negation_pattern + r')\s+' + re.escape(trigger)
    return re.search(pattern, text, re.IGNORECASE) is not None

# Function to determine the type
def determine_type(text, exclude_word=None):
    text = "" if not isinstance(text, str) else text
    
    if exclude_word:
        text = text.replace(exclude_word, "")
    if re.search(increase_pattern, text, re.IGNORECASE):
        return 'Increase'
    elif re.search(decrease_pattern, text, re.IGNORECASE):
        return 'Decrease'
    else:
        return 'Neutral'

def determine_row_type(row):
    trigger = row['trigger']
    arg0 = row['arg0_np']
    arg1 = row['arg1_np']
    
    # Determine COVt
    COVt = determine_type(trigger)
    
    # Determine COV0
    COV0 = determine_type(arg0)
    
    # Determine COV1, excluding the trigger word for evaluation
    COV1 = determine_type(arg1, exclude_word=trigger)
    
    return pd.Series([COV0, COVt, COV1])

# Apply the function to create new columns
df[['COV0', 'COVt', 'COV1']] = df.apply(determine_row_type, axis=1)

def determine_result_type(row):
    trigger = row['trigger']
    sentence = row['sent_text']

    if has_negation_before_trigger(sentence, trigger):
        return 'not_correlated'
    elif row['COV0'] == 'Increase' and row['COVt'] == 'Increase' and row['COV1'] == 'Neutral':
        return 'positively_correlated'
    elif row['COV0'] == 'Increase' and row['COVt'] == 'Decrease' and row['COV1'] == 'Neutral':
        return 'negatively_correlated'
    elif row['COV0'] == 'Decrease' and row['COVt'] == 'Increase' and row['COV1'] == 'Neutral':
        return 'negatively_correlated'
    elif row['COV0'] == 'Decrease' and row['COVt'] == 'Decrease' and row['COV1'] == 'Neutral':
        return 'positively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Increase' and row['COV1'] == 'Neutral':
        return 'positively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Decrease' and row['COV1'] == 'Neutral':
        return 'negatively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Neutral' and row['COV1'] == 'Neutral':
        return 'correlated_not_specified'
    elif row['COV0'] == 'Increase' and row['COVt'] == 'Neutral' and row['COV1'] == 'Neutral':
        return 'correlated_not_specified'
    elif row['COV0'] == 'Decrease' and row['COVt'] == 'Neutral' and row['COV1'] == 'Neutral':
        return 'correlated_not_specified'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Neutral' and row['COV1'] == 'Increase':
        return 'positively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Neutral' and row['COV1'] == 'Decrease':
        return 'negatively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Increase' and row['COV1'] == 'Increase':
        return 'positively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Increase' and row['COV1'] == 'Decrease':
        return 'negatively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Decrease' and row['COV1'] == 'Increase':
        return 'negatively_correlated'
    elif row['COV0'] == 'Neutral' and row['COVt'] == 'Decrease' and row['COV1'] == 'Decrease':
        return 'positively_correlated'
    elif row['COV0'] == 'Increase' and row['COVt'] == 'Neutral' and row['COV1'] == 'Increase':
        return 'positively_correlated'
    elif row['COV0'] == 'Increase' and row['COVt'] == 'Neutral' and row['COV1'] == 'Decrease':
        return 'negatively_correlated'
    elif row['COV0'] == 'Decrease' and row['COVt'] == 'Neutral' and row['COV1'] == 'Increase':
        return 'negatively_correlated'
    elif row['COV0'] == 'Decrease' and row['COVt'] == 'Neutral' and row['COV1'] == 'Decrease':
        return 'positively_correlated'
    else:
        return 'Inconclusive'

# Add Result_Type column
df['relation_type'] = df.apply(determine_result_type, axis=1)

# Drop COV0, COVt, and COV1 columns
df = df.drop(columns=['COV0', 'COVt', 'COV1'])

# Save the updated dataframe back to Excel
df.to_excel('/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Outputs/Abstract/rel_abs_more_Apr19_outputV3.xlsx', index=False)  
