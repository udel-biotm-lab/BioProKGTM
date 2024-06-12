import sys
from Bio import Entrez
import pandas as pd
import re
import os

Entrez.email = 'xxx@gmail.com'     # Enter your email

def format_sub_and_sup(text):
    # Remove <sub> and </sub> tags, retaining the content inside
    text = re.sub(r'<sub>(.*?)</sub>', r'\1', text)
    
    # Remove <sup> and </sup> tags, retaining the content inside
    text = re.sub(r'<sup>(.*?)</sup>', r'\1', text)
    
    return text

def fetch_abstracts_and_titles(pub_ids):
    batch = 1000
    # Make sure requests to NCBI are not too big
    for i in range(0, len(pub_ids), batch):
        j = i + batch
        if j >= len(pub_ids):
            j = len(pub_ids)

        print(f"Fetching abstracts and titles from {i} to {j}.")
        handle = Entrez.efetch(db="pubmed", id=','.join(pub_ids[i:j]),
                               rettype="xml", retmode="text", retmax=batch)

        records = Entrez.read(handle)

        data = []
        for pubmed_article in records['PubmedArticle']:
            pub_id = pubmed_article['MedlineCitation']['PMID']

            title = pubmed_article['MedlineCitation']['Article']['ArticleTitle']
            abstract = ''  # Initialize abstract as an empty string
            if 'Abstract' in pubmed_article['MedlineCitation']['Article'].keys():
                abstract_texts = pubmed_article['MedlineCitation']['Article']['Abstract']['AbstractText']
                # Join all sections of the abstract
                abstract = " ".join([str(text) for text in abstract_texts])
            
            data.append({'PMID': pub_id, 'Title': title, 'Abstract': abstract})
        
    return data

def save_abstract_to_file(row, folder_path):
    title = format_sub_and_sup(row['Title'])
    abstract = format_sub_and_sup(row['Abstract'])
    pmid = row['PMID']
    filename = f"{pmid}.txt"  # Customize the filename as per your requirement
    filepath = os.path.join(folder_path, filename)  # Combine folder path and filename
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(title + ' ' + abstract)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <email> <pmid_file_path> <output_folder_path>")
        sys.exit(1)
    
    email = sys.argv[1]
    pmid_file_path = sys.argv[2]
    output_folder_path = sys.argv[3]

    Entrez.email = email

    with open(pmid_file_path, 'r') as file:
        pmids = file.read().splitlines()
    
    all_data = []
    batch_size = 1000
    for i in range(0, len(pmids), batch_size):
        j = i + batch_size
        if j >= len(pmids):
            j = len(pmids)

        batch_pmids = pmids[i:j]
        batch_data = fetch_abstracts_and_titles(batch_pmids)
        all_data.extend(batch_data)

    merged_df = pd.DataFrame(all_data)

    for index, row in merged_df.iterrows():
        save_abstract_to_file(row, output_folder_path)
    # merged_df.to_excel('/home/shovan/Waters/query_result.xlsx', index=False)
