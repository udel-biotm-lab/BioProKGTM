# Text Mining Pipeline

This project involves setting up the text mining environment and performing various text mining tasks. Below are the steps to set up the environment and execute the necessary scripts.

## Table of Contents

1. [Step 0: Creating a Python3 Virtual Environment and Setting Up Required Packages](#step-0-creating-a-python3-virtual-environment-and-setting-up-required-packages)
2. [Step 1: Extracting Input Text Files](#step-1-extracting-input-text-files)
   - [Step 1.1: Extracting Abstracts](#step-11-extracting-abstracts)
   - [Step 1.2: Parsing Full-Length Articles](#step-12-parsing-full-length-articles)
   - [Step 1.3: Parsing Book Chapters](#step-13-parsing-book-chapters)
3. [Step 2: Ontological Concept Creation](#step-2-ontological-concept-creation)
4. [Step 3: Dictionary Concept Creation](#step-3-dictionary-concept-creation)
   - [Step 3.1: Acronym detection](#step-31-acronym-detection)
   - [Step 3.2: Import in a spreadsheet](#step-32-import-in-spreadsheet)
5. [Step 4: Concepts to Dictionary Mapping](#step-4-concepts-to-dictionary-mapping)
6. [Step 5: Setting Up EDG Tool](#step-5-setting-up-edg-tool)
   - [Step 5.1: Set Up nlputils](#step-51-set-up-nlputils)
   - [Step 5.2: Set Up EDG](#step-52-set-up-edg)
7. [Step 6: Running the EDG Tool for Argument Extraction](#step-6-running-the-edg-tool-for-argument-extraction)
9. [Step 7: Matching Dictionary Terms](#step-7-matching-dictionary-terms)
9. [Step 8: Postprocessing the Output Excel Sheet](#step-8-postprocessing-the-output-excel-sheet)
   - [Step 8.1: Post-process 1](#step-81-post-process-1)
   - [Step 8.2: Post-process 2](#step-82-post-process-2)
10. [Step 9: Adding Relation Types](#step-9-adding-relation-types)
11. [Step 10: Adding Sections and Chapters](#step-10-adding-sections-and-chapters)
   - [Step 10.1: Adding Sections for Full-Length Articles](#step-101-adding-sections-for-full-length-articles)
   - [Step 10.2: Adding Chapters for Book Chapters](#step-102-adding-chapters-for-book-chapters)


## Step 0: Creating a Python3 Virtual Environment and Setting Up Required Packages

1. Navigate to your project directory:
    ```bash
    cd /your_path/textmining
    ```

2. Install virtual environment:
    ```bash
    pip install virtualenv
    ```

3. Create a virtual environment:
    ```bash
    virtualenv -p /usr/bin/python3.8 myenv
    ```

4. Activate the virtual environment:
    ```bash
    source myenv/bin/activate
    ```

5. Check the Python version:
    ```bash
    python --version
    ```

6. Install the required packages:
    ```bash
    pip install -r /textmining/requirements.txt
    ```

    **Note**: If `pip` does not work, try using `pip3`.

## Step 1: Extracting Input Text Files

### Step 1.1: Extracting Abstracts

1. Create a directory to store text files and a text file with a list of PMIDs.
2. Run the `abstract_extract.py` script. We used Biopython’s Entrez API for this.
3. Successful execution of this script will create a folder that contains all the text abstracts for the given PMIDs.

    The script can be found in: `/textmining/scripts/input_text/`

    Run the script in the terminal:
    ```bash
    python3 abstract_extract.py xxx@gmail.com input_pmid.txt output_directory
    ```

    Change the email, PMIDs file, and output directory path in your terminal.

    Example: 
    ```bash
    python3 /textmining/scripts/input_text/abstract_extract.py xxx@gmail.com /textmining/Input/pmids.txt /textmining/Input/Abstract
    ```

    Example PMIDs file can be found in: `/textmining/Input/pmids.txt`
    
    Example output directory can be found in: `/textmining/Input/Abstract`

### Step 1.2: Parsing Full-Length Articles

1. Download all the BioCXML files for the PMC articles into a folder.
2. Create a directory to store text files for each PMC ID and another directory to store a spreadsheet containing the PMC ID, individual sentences, and the corresponding section from where the sentence was taken.
3. Run the `full_length_article_extract.py` script to parse the BioCXML files and extract the text portion for each full-length article as well as obtain the spreadsheet.

    The script can be found in: `/textmining/scripts/input_text/`

    Run the script in the terminal:
    ```bash
    python3 full_length_article_extract.py input_directory output_directory1 output_directory2
    ```

    Change the input and output directory paths in your terminal.

    Example: 
    ```bash
    python3 /textmining/scripts/input_text/full_length_article_extract.py /textmining/Input/Full_Length_Article_XML /textmining/Input/Full_Length_Text /textmining/Input/Full_Length_Section
    ```

    Example input directory can be found in: `/textmining/Input/Full_Length_Article_XML`
    
    Example output directory 1 can be found in: `/textmining/Input/Full_Length_Text`
    
    Example output directory 2 can be found in: `/textmining/Input/Full_Length_Section`

### Step 1.3: Parsing Book Chapters

#### Step 1.3.1: PDF Processing

1. Create a directory to store the PDF chapters.
2. Split the entire book into chapters and store it in a directory with the script `pdf_processing.py`.

    Successful execution of this script will split the book into chapters with a `.pdf` extension.

    **Note**: In the script, change the `source_pdf_path` in line 5 with the actual path of the book, change the `base_output_pdf_path` by giving the directory path for the output PDF chapters, change the range of pages by observing the page numbers of the book manually and add them accordingly in line 10.

    The script can be found in: `/textmining/scripts/input_text/Book/`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/input_text/Book/pdf_processing.py
    ```

    Example input directory can be found in: `/textmining/Input/book_chapters_pdf`

#### Step 1.3.2: Processing PDF to Text

1. Clone the `s2orc-doc2text` repository:
    ```bash
    git clone git@github.com:manju-anandakrishnan/s2orc-doc2text.git
    ```

2. Follow the instructions in the README file of this repository to process PDF to text.
3. After activating the virtual environment, navigate to the script directory and run the bash file:
    ```bash
    bash run_grobid.sh
    ```

4. Keep the server running and open another terminal to process the PDF files.
5. Set the Python path:
    ```bash
    export PYTHONPATH=/your_path/s2orc-doc2text
    ```

6. Navigate to the script directory and run the script:
    ```bash
    python /your_path/s2orc-doc2text/doc2text/process_pdf_text.py -i /textmining/Input/book_chapters_pdf/ -t temp_dir/ -o /textmining/Input/Book
    ```

    Example:
    ```bash
    python /your_path/s2orc-doc2text/doc2text/process_pdf_text.py -i /textmining/Input/book_chapters_pdf/ -t /textmining/Input/temp_dir/ -o /textmining/Input/Book
    ```

    Example input directory can be found in: `/textmining/Input/book_chapters_pdf`
    
    Example output text files can be found in: `/textmining/Input/Book`

#### Step 1.3.3: Split Large Text Files into Chunks

1. Run the script `split_text_into_chunks.py` to split large text files into multiple chunks.
2. The script can be found in: `/textmining/scripts/input_text/Book/`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/input_text/Book/split_text_into_chunks.py input_dir output_dir
    ```

    Example:
    ```bash
    python3 /textmining/scripts/input_text/Book/split_text_into_chunks.py /textmining/Input/Book /textmining/Input/Processed_Text_Book
    ```

    Example input directory can be found in: `/textmining/Input/Book`
    
    Example output directory can be found in: `/textmining/Input/Processed_Text_Book`

## Step 2: Ontological Concept Creation

1. Look into the current ontology first and add or change manually if necessary.
2. The current ontology can be found in: `/textmining/Concepts_and_Dictionary/Ontology_V1.xlsx`
3. Based on that, manually edit the consolidated type and type IDs of the ontology available in: `/textmining/Concepts_and_Dictionary/type_type_id.xlsx`

## Step 3: Dictionary Concept Creation

1. We already have current dictionary concepts available as a .obo file named `concepts.obo`.
2. This file can be found in: `/textmining/Concepts_and_Dictionary/concepts.obo`
3. For creating new concepts to the current file, run the script `adding_new_concepts.py` and follow the user-defined instruction in the terminal to add, update, or delete concepts to the dictionary.

    **Note**: Make sure to change the path of the spreadsheet created in Step 2 in line 184 and the path to the concept file in line 188.

    The script can be found in: `/textmining/scripts/Concepts`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/Concepts/adding_new_concepts.py
    ```

    While running the script, follow the instructions in the terminal carefully. Use all uppercase letters for abbreviations (e.g., ADCC for antibody-dependent cellular cytotoxicity). Add the plural forms if necessary for any specific canonical name or alternative names. Make sure to exit by pressing "E" after any Add, Update, or Delete operation.

### Step 3.1: Acronym detection

1. If you want to know the acronyms across text and add concepts of them, you have to use the acronym detector tool.
2. Clone the github repository and follow the setup instructions given there.
   ```bash
    git clone git@github.com:ncbi-nlp/Ab3P.git
    ```
3. Once you complete the setup process, run the script run_acronym.py to get all the long forms and short forms of the terms available in the text.
4. Successful running of this script will create a .txt file that will have the processed text having the acronyms available in the processed text. N.B: make sure to set the correct path for ./identify_abbr in line 24 as an external script is used here that detects the acronyms.
   
   The script can be found in: `/textmining/scripts/Concepts`

   Run the script in the terminal:
    ```bash
    python3 run_acronym.py /your_path/input_dir /your_path/output_dir/acronym_output.txt
    ```

   Example input_dir can be found in: `/textmining/Input/Abstract`
   
   Example acronym_output.txt file can be found in: `/textmining/Concepts_and_Dictionary/Acronym/acronym_output.txt`

### Step 3.2: Import in a spreadsheet 
If you want to import the text output to an Excel spreadsheet for better visualization, run the SF_LF.py script.

   The script can be found in: `/textmining/scripts/Concepts`

   Run the script in the terminal:
    ```bash
    python3 SF_LF.py /your_path/acronym_output.txt /your_path/excel_output.xlsx
    ```

   Example input_dir can be found in: `/textmining/Concepts_and_Dictionary/Acronym/acronym_output.txt`
   
   Example acronym_output.txt file can be found in: `/textmining/Concepts_and_Dictionary/Acronym/sf_lf.xlsx`


## Step 4: Concepts to Dictionary Mapping

1. Run the script `obo_to_dict_map.py` to map dictionary terms from the concept OBO format to a JSON format.
2. This JSON file is required to match dictionary terms from the noun phrases.

    The script can be found in: `/textmining/scripts/Concepts`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/Concepts/obo_to_dict_map.py input_file output_file
    ```

    Example:
    ```bash
    python3 /textmining/scripts/Concepts/obo_to_dict_map.py /textmining/Concepts_and_Dictionary/concepts.obo /textmining/Concepts_and_Dictionary/transformed_data1.json
    ```

    Example input file can be found in: `/textmining/Concepts_and_Dictionary/concepts.obo`
    
    Example output file can be found in: `/textmining/Concepts_and_Dictionary/transformed_data1.json`

## Step 5: Setting Up EDG Tool

### Step 5.1: Set Up nlputils

1. Get access to the GitHub repository: [nlputils](https://github.com/udel-biotm-lab/nlputils)
2. Clone the repository:
    ```bash
    git clone git@github.com:udel-biotm-lab/nlputils.git
    ```

3. Follow the steps in the `README.md`, starting from the heading “Initialization”. When running `clear_init.sh`, if there is any error not having a `dep` directory, create it using:
    ```bash
    mkdir -p dep
    ```

4. The `init.sh` execution may run into an error on execution of the `make check` command. If this happens, run the commands from line 62 to line 93 in `init.sh` individually in the terminal. To do this:
    - Change to directory `dep/protobuf` in the terminal.
    - Execute lines 62 to 87 in `init.sh`.
    - Instead of line 88, execute the command:
        ```bash
        pip install grpcio==1.20.0
        ```
    - Continue executing from line 89 to 93.
    - Verify if the directory path `${ROOT_PATH}/grpc-java/compiler/build/exe/java_plugin` exists. If not, create the directory path:
        ```bash
        mkdir -p ${ROOT_PATH}/grpc-java/compiler/build/exe/java_plugin
        ```

5. Ensure you are in the `dep/grpc-java/compiler` directory, then download the Java plugin into the path `build/exe/java_plugin` using the below command:
    ```bash
    wget https://search.maven.org/remotecontent?filepath=io/grpc/protoc-gen-grpc-java/1.6.1/protoc-gen-grpc-java-1.6.1-linux-x86_64.exe -O build/exe/java_plugin/protoc-gen-grpc-java
    ```

6. Change the access level for the downloaded plugin:
    ```bash
    chmod +x protoc-gen-grpc-java
    ```

7. Execute the below commands:
    ```bash
    pip install -U shortuuid
    pip install -U bllipparser
    pip install -U glog
    ```

8. Continue with steps after `init.sh` as in `README.md`.
9. On successful setup, execute:
    ```bash
    python test/example.py
    ```
    **Note**: It might take some time.

10. If you run into issues, verify the `run.sh` in the `docker` folder for correct port numbers of BLLIP_PORT and STANFORD_PORT. (BLLIP – 8902, STANFORD – 8900). If they do not work, confirm the port numbers with the project maintainers.

### Step 5.2: Set Up EDG

1. Follow the steps in the repository: [Steps_for_new_projects_usingEDG_andMongoDB](https://github.com/udel-biotm-lab/Steps_for_new_projects_usingEDG_andMongoDB)
2. Follow step 7 – “Run EDG framework on README.md”.
3. On successful execution of the python file, verify the repository for the `test_cair_single.tsv` file.
4. Every time you run next, make sure you have your virtual environment activated for the `nlputils` and have:
    ```bash
    . ./scripts/export_path.sh
    ```

## Step 6: Running the EDG Tool for Argument Extraction

1. After testing whether the EDG system is working properly, run the script `RE_Script_For_Argument_Extraction.py` to generate the first output spreadsheet with extracted relations.
2. Use the JSON file created in Step 4 in line 307.
3. Successful running of this script will generate a spreadsheet as an output as well as a TSV file. The spreadsheet will contain the dictionary matches and their corresponding types and concept IDs. However, the TSV file will only have the arguments for extracted relations.

    The script can be found in: `/textmining/scripts/EDG`

    Run the script in the terminal:
    ```bash
    python2 /textmining/scripts/EDG/RE_Script_For_Argument_Extraction.py input_dir rule_dir > output_tsv
    ```

    **Note**: This script is in Python 2 because of the dependency of `nlputils`. So please switch to Python 2 virtual environment before running this script.

    Example:
    ```bash
    python2 /textmining/scripts/EDG/RE_Script_For_Argument_Extraction.py /textmining/Input/Abstract /textmining/Rules > /textmining/Outputs/tsv/abstract_relations.tsv
    ```

    Example input directory can be found in: `/textmining/Input/Abstract`
    
    Example rule directory can be found in: `/textmining/Rules`
    
    Example TSV outputs can be found in: `/textmining/Outputs/tsv`

## Step 7: Matching Dictionary Terms

1. Run the script `adding_dictionary_matches_after_running_edg.py` to match the dictionary terms and their corresponding types and concept IDs from the arguments involved in relations.
2. This step is essential whether you run Step 6 or not. If it is not necessary to run the RE tool, you can skip Step 6 and directly run Step 7 that involves having a previous spreadsheet generated from Step 6, input dictionary file generated from Step 4, and outputs a spreadsheet that matches dictionary terms from argument noun phrases.

    The script can be found in: `/textmining/scripts/EDG`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG/adding_dictionary_matches_after_running_edg.py /your_path/input_excel.xlsx /your_path/dictionary.json /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG/adding_dictionary_matches_after_running_edg.py /textmining/Outputs/Abstract/TP_OutputV3.xlsx /textmining/Concepts_and_Dictionary/transformed_data1.json /textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx
    ```

    Example input excel can be found in: `/textmining/Outputs/Abstract/TP_OutputV3.xlsx`
    
    Example dictionary JSON can be found in: `/textmining/Concepts_and_Dictionary/transformed_data1.json`
    
    Example output excel can be found in: `/textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx`

## Step 8: Postprocessing the Output Excel Sheet

### Step 8.1: Post-process 1

1. We need some post-processing in this step to eliminate some errors and deal with multiple matches.
2. Run the script `post_process1.py` first. This will have an input of an excel sheet that is generated in Step 7 as output and the output will be used in Step 8.2.

    The script can be found in: `/textmining/scripts/EDG_Output_Process`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/post_process1.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/post_process1.py /textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx /textmining/Outputs/Abstract/abs_more_Apr19_outputV3.xlsx
    ```

    Example input excel can be found in: `/textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx`
    
    Example output excel can be found in: `/textmining/Outputs/Abstract/abs_more_Apr19_outputV3.xlsx`

### Step 8.2: Post-process 2

1. Run the script `post_process2.py` to remove duplicate rows generated because of having the same relations for multiple rules.
2. Here, the input will be the output excel sheet from Step 8.1 and the output will be another excel sheet used in Step 9.

    The script can be found in: `/textmining/scripts/EDG_Output_Process`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/post_process2.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/post_process2.py /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV3.xlsx /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx
    ```

    Example input excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV3.xlsx`
    
    Example output excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx`

## Step 9: Adding Relation Types

1. Run the script `adding_relation_types.py` to add a new column named `Relation_Type` in the excel sheet generated in Step 8.
2. You can use the output script generated in Step 8 and update in the same script or output a different excel sheet.

    The script can be found in: `/textmining/scripts/EDG_Output_Process`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/adding_relation_types.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/adding_relation_types.py /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV5.xlsx
    ```

    Example input excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx`
    
    Example output excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV5.xlsx`

## Step 10: Adding Sections and Chapters

### Step 10.1: Adding Sections for Full-Length Articles

1. If you want to add sections for the full-length articles, run the script `section_addition_for_full_length.py` to add a column `section` in the output excel sheet.
2. Here, the first input will be the output from Step 9 and the second input will be the spreadsheet generated in Step 1.3. The output excel generated here is ready to transfer to the knowledge graph.

    The script can be found in: `/textmining/scripts/EDG_Output_Process`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/section_addition_for_full_length.py /your_path/input_excel_1.xlsx /your_path/input_excel_2.xlsx /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/section_addition_for_full_length.py /textmining/Outputs/Full_Length/rel_Apr14_outputV2.xlsx /textmining/Input/Full_Length_Section/extracted_sentences_sections_docIds.xlsx /textmining/Outputs/Full_Length/sec_rel_Apr14_outputV2.xlsx
    ```

    Example input excel 1 can be found in: `/textmining/Outputs/Full_Length/rel_Apr14_outputV2.xlsx`
    
    Example input excel 2 can be found in: `/textmining/Input/Full_Length_Section/extracted_sentences_sections_docIds.xlsx`
    
    Example output excel can be found in: `/textmining/Outputs/Full_Length/sec_rel_Apr14_outputV2.xlsx`

### Step 10.2: Adding Chapters for Book Chapters

1. If you want to add chapters instead of sections for the book chapters, run the script `chapter_addition_for_book_chapters.py` to add a column `section` in the output excel sheet.
2. Here, the input will be the output from Step 9 and the output excel generated here is ready to transfer to the knowledge graph.

    The script can be found in: `/textmining/scripts/EDG_Output_Process`

    Run the script in the terminal:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/chapter_addition_for_book_chapters.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx
    ```

    Example:
    ```bash
    python3 /textmining/scripts/EDG_Output_Process/chapter_addition_for_book_chapters.py /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV5.xlsx
    ```

    Example input excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx`
    
    Example output excel can be found in: `/textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV5.xlsx`
