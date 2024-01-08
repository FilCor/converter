import sys
import fitz  # PyMuPDF

def convert_pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    
    for page_num in range(len(doc)):
        page = doc[page_num]  # Carica la pagina
        text += page.get_text()
    
    doc.close()
    return text

def save_text_to_file(text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Testo salvato con successo in {output_path}")

if __name__ == "__main__":
    try:
        pdf_path = sys.argv[1]
        text = convert_pdf_to_text(pdf_path)
        output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"  # Default output filename
        save_text_to_file(text, output_path)
    except Exception as e:
        print(e)
        print("Inserire il percorso del file PDF come argomento e, opzionalmente, il percorso del file di output.")
