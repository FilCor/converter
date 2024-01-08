import csv
import openpyxl
import sys
import os

def csv_to_excel(csv_file_path, excel_file_path=None):
    # Se non viene fornito un percorso specifico per il file Excel, crealo nella stessa directory del file CSV con estensione .xlsx
    if excel_file_path is None:
        dir_name, base_name = os.path.split(csv_file_path)
        name, _ = os.path.splitext(base_name)
        excel_file_path = os.path.join(dir_name, name + ".xlsx")

    wb = openpyxl.Workbook()
    sheet = wb.active
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            sheet.append(row)
    
    wb.save(excel_file_path)
    print(f"File Excel salvato con successo in: {excel_file_path}")

if __name__ == "__main__":
    try:
        csv_file_path = sys.argv[1]
        excel_file_path = None
        if len(sys.argv) > 2:
            excel_file_path = sys.argv[2]
        csv_to_excel(csv_file_path, excel_file_path)
    except Exception as e:
        print(e)
        print("Errore durante la conversione di CSV in Excel")
