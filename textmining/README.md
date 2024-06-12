Step 0: Creating python3 virtual environment and setting up the required packages

In this project, we used python version 3.8.15. You can create a virtual environment for python 3.

For example:
cd /your_path/textmining
  
Insall virtual environment: pip install virtualenv
Create a virtual environment: virtualenv -p /usr/bin/python3.8 myenv
Activate the virtual environment: source myenv/bin/activate
Check the version: python --version

Install the packages by: pip install -r requirements.txt
N.B: In case pip does not work, try with pip3

requirement.txt file can be found in: /textmining/requirements.txt


Step 1: Extracting input text files

Step 1.1: Extracting abstracts 
Create a directory to store text files and a text file with a list of pmids. Run the abstract_extract.py script. We used Biopython’s Entrez API for this. Successful running of this script will create a folder that contains all the text abstracts for the given pmids.

The script can be found in: /textmining/scripts/input_text/

Run the script in the terminal:
python3 abstract_extract.py xxx@gmail.com input_pmid.txt output_directory
Change the email, pmid file and output_directory path in your terminal.
You can find the script in: /textmining/scripts/input_text/abstract_extract.py
Example pmid file can be found in: /textmining/Input/pmids.txt
Example output directory can be found in: /textmining/Input/Abstract


Step 1.2: Parsing full-length articles:
Download all the biocXML files for the PMC articles in a folder. Create a directory to store text files for each pmcid and another directory to store a spreadsheet containing the pmcid, individual sentences and the corresponding section from where the sentence was taken. Run the full_length_article_extract.py script to parse the biocXML files and extract the text portion for each full-length article as well as to obtain the spreadsheet. The spreadsheet is essential for later usage of adding sections of the relations in Step 10.1. 
N.B: We only considered title, abstract and result sections of the full length articles.

The script can be found in: /textmining/scripts/input_text/

Run the script in the terminal:
python3 full_length_article_extract.py input_directory output_directory1 output_directory2
Change the input and output directory paths in your terminal
Example input directory can be found in: /textmining/Input/Full_Length_Article_XML
Example output directory1 can be found in: /textmining/Input/Full_Length_Text
Example output directory2 can be found in: /textmining/Input/Full_Length_Section




Step 1.3: Parsing book chapters:

Step 1.3.1: Pdf processing: 
Create a directory to store the pdf chapters. Split the entire book into chapters and store it in a directory with the script pdf_processing.py
Successful running of this script will split the book into chapters with a .pdf extension. 
N.B: In the script, change the source_pdf_path in line 5 with the actual path of the book, change the base_output_pdf_path by giving the directory path for the output pdf chapters, change the range of pages by observing the page numbers of the book manually and add them accordingly in line 10.

The script can be found in: /textmining/scripts/input_text/Book/

Run the script in the terminal:
Python3 pdf_processing.py

Example directory can be found in: /textmining/Input/book_chapters_pdf

Step 1.3.2: Processing PDF to Text
git clone git@github.com:manju-anandakrishnan/s2orc-doc2text.git
Follow the instructions in the readme file of this repository to process pdf to text
After activating the virtual environment, cd /your_path/s2orc-doc2text/scripts and run the bash file by the command: bash run_grobid.sh
Please keep the server running and open another terminal to process the pdf files.
cd /your_path/s2orc-doc2text
Set python path by the command: export PYTHONPATH=/your_path/s2orc-doc2text
cd /your_path/s2orc-doc2text/doc2text
Run the script in the terminal: 
python process_pdf_text.py -i /textmining/Input/book_chapters_pdf/ -t temp_dir/ -o /textmining/Input/Book
Here, example input directory is the output directory from step 1 and example output text files can be put into Book directory. Please, create the output directory before you run the script.

Step 1.3.3: Split large text files into chunks
Once you get the text files from Step 2, you might need to split the large text files into chunks for processing the text documents by the relation extraction tool. Run the script split_text_into_chunks.py to split the large text files into multiple chunks. 
The script can be found in: /textmining/scripts/input_text/Book/
Run the script in the terminal:
Python3 split_text_into_chunks.py input_dir output_dir
Example input_dir can be found in: /textmining/Input/Book
Example output_dir can be found in: /textmining/Input/Processed_Text_Book


Step 2: Ontological Concept Creation
Look into the current ontology first and add or change manually if necessary. The current ontology can be found in:  /textmining/Concepts_and_Dictionary/Ontology_V1.xlsx

Based on that manually edit the consolidated type and type ids of the ontology available in: /textmining/Concepts_and_Dictionary/type_type_id.xlsx

This file is essential to create dictionary concepts as well.

Step 3: Dictionary Concept Creation
We already have a current dictionary concepts available as a .obo file named “concepts.obo”. This file can be found in:  /textmining/Concepts_and_Dictionary/concepts.obo
For creating new concepts to the current file, Run the script adding_new_concepts.py and follow the user defined instruction in the terminal to add, update or delete concepts to the dictionary. Although you can add manually with unique concept id inside the concept file, we STRONGLY recommend to use the script to avoid any mistakes.
Successful running of the adding_new_concepts.py script will add new concepts to the current file as well as update or delete concepts from the current file. 
Make sure to change the path of the spreadsheet created in Step 2 in line 184 and the path to the concept file in line 188.

While running the script, the user will be asked to give inputs. Follow the instructions in the terminal carefully. First, press “A” if you want to add new concept. Similarly, you can update (U) or delete (D) the canonical name or it’s corresponding alternative names as well as type ids. Please ensure the type ids in the spreadsheet created in step 2 before considering to add them to the dictionary concept. Make sure to exit by pressing “E” after any of the Add, Update or Delete operation. 
When you will run the script, make sure to use all UPPERCASE letters for the abbreviations (For example, ADCC which is the abbreviation for antibody dependent cellular cytotoxicity). Also, add the plural forms if necessary for any specific canonical name or alternative names. 

The script can be found in: /textmining/scripts/Concepts

Run the script in the terminal:
python3 adding_new_concepts.py

Step 4: Concepts to Dictionary Mapping
To create the dictionary terms with their corresponding concept id and types, run the script obo_to_dict_map.py that maps these items from the concept obo format to a json format. This json file is required to match dictionary terms from the noun phrases. here , the input will be the concept OBO file created in Step 3 and output will be a json file.

The script can be found in: /textmining/scripts/Concepts
Run the script in the terminal:
python3 obo_to_dict_map.py input_file output_file
Example input file can be found in: /textmining/Concepts_and_Dictionary/concepts.obo
Example output file can be found in: /textmining/Concepts_and_Dictionary/transformed_data1.json

Step 5: Setting up EDG tool
Step 5.1:  Set up nlputils 
1. Get access to the github repository - https://github.com/udel-biotm-lab/nlputils 
2. Clone git@github.com:udel-biotm-lab/nlputils.git 
3. Follow the steps in README.md, starting from the heading “Initialization”. When running clear_init.sh, if there is any error not having a dep directory, create it using mkdir -p dep (under nlputils)
4. init.sh execution may run into error on execution of the ‘make check’ command. If this  happens, run the commands from line 62 to line 93 in init.sh individually in the terminal. 
To do this, change to directory ‘dep/protobuf’ in the terminal.
Execute lines 62 to 87 in init.sh.
Instead of line 88, execute the command, ‘pip install grpcio==1.20.0’
Continue executing from line 89 to 93.
Verify if the directory path, “${ROOT_PATH}/grpc- java/compiler/build/exe/java_plugin” exists. If this path doesn’t exist create the directory path, ${ROOT_PATH}/grpc- java/compiler/build/exe/java_plugin.
Ensure you are in “dep/grpc-java/compiler” directory, then, download the java plugin into the path, build/exe/java_plugin using  the below command,
wget https://search.maven.org/remotecontent?filepath=io/grpc/protoc-gen-grpc-java/1.6.1/protoc-gen-grpc-java-1.6.1-linux-x86_64.exe -O build/exe/java_plugin/protoc-gen-grpc-java 
   Change the access level for the downloaded plugin – “chmod +x protoc-gen-grpc-java” 
Execute the below three commands, 
pip install -U shortuuid 
pip install -U bllipparser 
pip install -U glog 
Continue with steps after init.sh as in README.md 
5. On successful set up of the steps, execute python test/example.py. It might take some time.
6. If you run into issues, verify the run.sh in docker folder for correct port numbers of  BLLIP_PORT and STANFORD_PORT. (BLLIP – 8902, STANFORD – 8900) 
If they do not work, confirm the port numbers with Manju/Dr. Chen. 
Step 5.2: Set up EDG  
Go to https://github.com/udel-biotm-lab/Steps_for_new_projects_usingEDG_andMongoDB 
2. Follow step 7 – “Run EDG framework on README.md” 
3. On successful execution of the python file, verify the repository for test_cair_single.tsv file.
4. Every time you run next, make sure you have your virtual environment activated for the nlputils and have “. ./scripts/export_path.sh” this exported

Step 6: Running the EDG tool for Argument Extraction
After testing whether the edg system is working properly, run the script RE_Script_For_Argument_Extraction.py to generate the first output spreadsheet with extracted relations. Use the json file created in Step 4 in line 307. Successful running of this script will generate a spreadsheet as an output as well as a tsv file. The spreadsheet will contain the dictionary matches and their corresponding types and concept ids. However, the tsv file will only have the arguments for extracted relations. This script will take two inputs. First input is the text file generated in Step 1 and the next input will be a rule folder. 

The script can be found in: /textmining/scripts/EDG

Run the script in the terminal:
python input_dir rule_dir > output_tsv
N.B: This script is in python 2 because of the dependency of nlputils. So please switch to python 2 virtual environment before running this script.

Example input_dir can be found in:  /textmining/Input/Abstract
Example rule_dir can be found in: /textmining/Rules
Example spreadsheet output can be found in: /textmining/Outputs/Abstract/abs_more_Apr19_outputV1.xlsx
Example tsv outputs can be found in: /textmining/Outputs/tsv

For different type of texts, use the input files accordingly for generating relations.

Step 7: Matching Dictionary terms with or without running Step 6
In this step, run the adding_dictionary_matches_after_running_edg.py script to match the dictionary terms and their corresponding types and concept ids from the arguments involved in relations. It is essential if you run Step 6 or not. If it is not necessary to run the RE tool, you can skip Step 6 and directly run Step 7 that involves having a previous spreadsheet generated from Step 6, input dictionary file generated from Step 4 and outputs a spreadsheet that matches dictionary terms from argument nps. 
The script can be found in: /textmining/scripts/EDG

Run the script in the terminal:
python3 adding_dictionary_matches_after_running_edg.py /your_path/input_excel.xlsx /your_path/dictionary.json /your_path/output_excel.xlsx

Example input_excel can be found in: /textmining/Outputs/Abstract/TP_OutputV3.xlsx
Example dictionary_json can be found in: /textmining/Concepts_and_Dictionary/transformed_data1.json
Example output_excel can be found in: /textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx

Step 8: Postprocessing of the output excel sheet 
Step 8.1: Post-process 1
We need some postprocessing in this step to eliminate some errors and deal with multiple matches. Run the script post_process1.py first. This will have an input of excel sheet that is generated in Step 7 as output and the output will be used in Step 8.2. 
The script can be found in: /textmining/scripts/EDG_Output_Process

Run the script in the terminal:
python3 post_process1 /your_path/input_excel.xlsx /your_path/output_excel.xlsx

Example input_excel can be found in: /textmining/Outputs/Abstract/updated_TP_OutputV3.xlsx
Example output_excel can be found in: /textmining/Outputs/Abstract/abs_more_Apr19_outputV3.xlsx

Step 8.2: Post-process 2
Run the script post_process2.py to remove same rows generated because of having the same relations for multiple rules. Here, the input will be the output excel sheet from Step 8.1 and the output will be another excel sheet used in Step 9.
The script can be found in: /textmining/scripts/EDG_Output_Process

Run the script in the terminal:
python3 post_process2 /your_path/input_excel.xlsx /your_path/output_excel.xlsx

Example input_excel can be found in: /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV3.xlsx
Example output_excel can be found in: /textmining/Outputs/Abstract/rel_abs_more_Apr19_outputV4.xlsx

Step 9: Adding Relation Types
Run the script adding_relation_types.py to add a new column named “Relation_Type in the excel sheet generated in Step 8. 
The script can be found in: /textmining/scripts/EDG_Output_Process

Run the script in the terminal:
python3 adding_relation_types.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx

You can use the output script generated in Step 8 and update in the same script or output a different excel sheet.

Step 10: Adding Sections and Chapters
Step 10.1: Adding sections for full length articles
If you want to add sections for the full-length articles, run the script section_addition_for_full_length.py to add a column “section” in the output excel sheet. Here, the first input will be the output from Step 9 and the second input will be the spreadsheet generated in Step 1.3. The output excel generated here is ready to transfer to the knowledge graph.
The script can be found in: /textmining/scripts/EDG_Output_Process

Run the script in the terminal:
python3 /your_path/input_excel_1.xlsx /your_path/input_excel_2.xlsx /your_path/output_excel.xlsx

Example input_excel_1 can be found in: /textmining/Outputs/Full_Length/rel_Apr14_outputV2.xlsx

Example input_excel_2 can be found in: /textmining/Input/Full_Length_Section/extracted_sentences_sections_docIds.xlsx
Example output_excel can be found in: /textmining/Outputs/Full_Length/sec_rel_Apr14_outputV2.xlsx

Step 10.2: Adding chapters for book chapters
If you want to add chapters instead of sections for the book chapters, run the script chapter_addition_for_book_chapters.py to add a column “section” in the output excel sheet. Here, the input will be the output from Step 9 and the output excel generated here is ready to transfer to the knowledge graph.
The script can be found in: /textmining/scripts/EDG_Output_Process

Run the script in the terminal:
python chapter_addition_for_book_chapters.py /your_path/input_excel.xlsx /your_path/output_excel.xlsx
You can use the same excel input and update it to get the output.
