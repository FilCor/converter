import fitz  # PyMuPDF
import os

def extract_pages(pdf_path, page_numbers, output_path):
    doc = fitz.open(pdf_path)
    writer = fitz.open()  # Documento vuoto in cui inserire le pagine estratte
    
    for page_num in page_numbers:
        if page_num < len(doc):  # Assicurati che il numero di pagina sia valido
            writer.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    writer.save(output_path)
    writer.close()
    doc.close()
