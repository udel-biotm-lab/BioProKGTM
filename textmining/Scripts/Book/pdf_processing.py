import PyPDF2
import os

# Define the source and base output directory
source_pdf_path = '/home/shovan/nlputils/EDG_framework/Waters/pdf/Cell Culture Bioprocess Engineering_2nd_edition chapters 3 and 4 annotations (1).pdf'
base_output_pdf_path = '/home/shovan/pdf_to_text/s2orc-doc2text/doc2text/pdf_repo'

# Specify the ranges of pages you want to keep (0-based index)
page_ranges_to_keep = [(14, 44), (50, 95), (98, 150), (154, 192), (196, 216), (220, 247), (252, 288), (292, 314), (318, 335), (340, 360), (364, 384), (388, 417)]

# Ensure the output directory exists
if not os.path.exists(base_output_pdf_path):
    os.makedirs(base_output_pdf_path)

# Open the source PDF file
with open(source_pdf_path, 'rb') as source_file:
    source_pdf = PyPDF2.PdfReader(source_file)
    
    # Counter for output file naming
    file_counter = 1
    
    # Iterate over each page range
    for start_page, end_page in page_ranges_to_keep:
        pdf_writer = PyPDF2.PdfWriter()  # Create a new PdfWriter for each range

        # Correctly process each range
        for page_num in range(start_page, end_page + 1):
            if page_num < len(source_pdf.pages):
                page = source_pdf.pages[page_num]
                pdf_writer.add_page(page)
            else:
                print(f"Page {page_num + 1} is out of bounds and was not added.")

        # Define a unique output file path for each range
        output_pdf_file_path = os.path.join(base_output_pdf_path, f"output_{file_counter}.pdf")
        file_counter += 1
        
        # Save the new PDF
        with open(output_pdf_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)
        print(f"Output PDF has been created: {output_pdf_file_path}")
