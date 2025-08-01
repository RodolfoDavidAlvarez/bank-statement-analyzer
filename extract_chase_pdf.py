import PyPDF2
import sys

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text

# Extract text from the PDF
pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Bank Statement NB Personal Account/20250108-statements-2084-.pdf"
extracted_text = extract_pdf_text(pdf_path)

print(extracted_text)