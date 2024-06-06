import os
import xml.etree.ElementTree as ET
import re

def extract_cdata(xml_content):
    # Extract CDATA content using regex
    cdata_regex = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    return cdata_regex.findall(xml_content)

def parse_inner_xml(cdata_contents):
    results = []
    temp_results = []  # To store paragraphs until we decide what to do
    section_flag = None  # To determine if we've hit 'CONCLUSION' or 'DISCUSSION'

    for content in cdata_contents:
        try:
            root = ET.fromstring(f'<root>{content}</root>')  # Encapsulate in a root for proper parsing
            for section in root.iter('section'):
                title_element = section.find('.//title[@type="main"]')
                title_text = title_element.text.upper() if title_element is not None and title_element.text else ""
                
                # Check for the presence of 'CONCLUSION' or 'DISCUSSION' in section titles
                if "CONCLUSION" in title_text:
                    section_flag = 'CONCLUSION'
                    temp_results = [p.text.strip() for p in section.findall('.//p') if p.text]
                    break
                elif "DISCUSSION" in title_text and not section_flag:
                    section_flag = 'DISCUSSION'
                    temp_results = [p.text.strip() for p in section.findall('.//p') if p.text]
                elif not section_flag:
                    # Collect paragraphs if no 'CONCLUSION' or 'DISCUSSION' has been flagged yet
                    paragraphs = [p.text.strip() for p in section.findall('.//p') if p.text]
                    results.extend(paragraphs)

            # Decide based on flags what to append to final results
            if section_flag == 'CONCLUSION' or (section_flag == 'DISCUSSION' and not 'CONCLUSION' in title_text):
                results.extend(temp_results)
                break

        except ET.ParseError as e:
            print(f"Error parsing CDATA content as XML: {e}")
            continue

    return results

def process_xml_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_path = os.path.join(directory, filename)
            with open(xml_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()

            # Extract CDATA and parse it
            cdata_contents = extract_cdata(xml_content)
            if cdata_contents:
                results = parse_inner_xml(cdata_contents)
                results_text = '\n\n'.join(results) if results else 'No results found'

                # Write results to a text file
                output_path = os.path.join(directory, filename.replace('.xml', '_results.txt'))
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(results_text)
                print(f"Processed {filename}")

# Directory where your XML files are stored
directory = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Full_Length_Litsuggest'
process_xml_files(directory)
