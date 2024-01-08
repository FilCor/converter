import pandas as pd
import sys
import os

def csv_to_json(csv_file_path, json_file_path=None):
    # Se non viene fornito un percorso specifico per il file JSON, crealo nella stessa directory del file CSV con estensione .json
    if json_file_path is None:
        dir_name, base_name = os.path.split(csv_file_path)
        name, _ = os.path.splitext(base_name)
        json_file_path = os.path.join(dir_name, name + ".json")
    
    try:
        data = pd.read_csv(csv_file_path)
        data.to_json(json_file_path, orient='records')
        print(f"File JSON salvato con successo in: {json_file_path}")
    except Exception as e:
        print("Errore durante la conversione:", e)

if __name__ == "__main__":
    try:
        csv_file_path = sys.argv[1]
        json_file_path = None
        if len(sys.argv) > 2:
            json_file_path = sys.argv[2]
        csv_to_json(csv_file_path, json_file_path)
    except Exception as e:
        print(e)
        print("Errore durante la conversione di CSV in JSON")
