import os
import xml.etree.ElementTree as ET
import re

def get_namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

def extract_data_from_xml(xml_path):
    # Parsing the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extracting namespace from root element
    namespace = get_namespace(root)
    ns = {'ns': namespace}

    # Extracting the article title
    title = root.find('.//ns:article-title', namespaces=ns)
    title_text = title.text.strip() if title is not None else 'No title found'

    # Extracting the abstract
    abstract = root.find('.//ns:abstract/ns:p', namespaces=ns)
    abstract_text = abstract.text.strip() if abstract is not None else 'No abstract found'

    # Extracting paragraphs from RESULTS section
    results = []
    sections = root.findall('.//ns:section', namespaces=ns)
    for section in sections:
        section_title = section.find('.//ns:title[@type="main"]', namespaces=ns)
        if section_title is not None and 'RESULTS' in section_title.text:
            print(f"Found RESULTS section: {section_title.text}")  # Debug print
            paragraphs = section.findall('.//ns:p', namespaces=ns)
            for p in paragraphs:
                results.append(p.text.strip())
                print(f"Found paragraph: {p.text.strip()}")  # Debug print

    results_text = '\n\n'.join(results) if results else 'No results found'

    # Combine all parts into a single string to return
    combined_text = f"Title: {title_text}\n\nAbstract: {abstract_text}\n\nResults:\n{results_text}"
    return combined_text

def process_xml_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_path = os.path.join(directory, filename)
            data = extract_data_from_xml(xml_path)
            # Writing data to a text file
            output_path = os.path.join(directory, filename.replace('.xml', '.txt'))
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(data)
            print(f"Processed {filename}")

# Directory where your XML files are stored
directory = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Full_Length_Litsuggest'
process_xml_files(directory)
