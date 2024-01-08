import sys
import os
import subprocess

def epub_to_awz3(file_path):
    if file_path.split(".")[-1].lower() == "epub":
        if os.path.isfile(file_path):
            output_path = file_path.rsplit('.', 1)[0] + ".azw3"
            try:
                subprocess.call(["ebook-convert", file_path, output_path])
            except Exception as e:
                print("Errore durante la conversione:", e)
        else:
            print("Percorso file non valido!")
    else:
        print("Estensione file non valida!")

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        epub_to_awz3(file_path)
        print("Conversione completata con successo!")
    except Exception as e:
        print(e)
        print("Inserisci il percorso del file Ebook come argomento da riga di comando!")
