from PyPDF2 import PdfMerger
import sys

def merge_pdfs(pdf_list, output_pdf):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    
    merger.write(output_pdf)
    merger.close()
    print("PDF uniti con successo in", output_pdf)
    return output_pdf  # Restituisce il percorso del file di output per ulteriori usi

if __name__ == "__main__":
    try:
        # La lista di PDF viene passata come argomenti (incluso il nome del file di output)
        pdf_list = sys.argv[1:-1]  
        output_pdf = sys.argv[-1]  # Nome del file di output come ultimo argomento
        merge_pdfs(pdf_list, output_pdf)
    except Exception as e:
        print(e)
        print("Inserire i percorsi dei file PDF da unire seguiti dal nome del file PDF di output.")
