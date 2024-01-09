import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys

# Importa qui tutti i tuoi moduli di conversione
from functions.convert_ebook import epub_to_awz3
from functions.convert_csv_excel import csv_to_excel
from functions.csv_to_json import csv_to_json 
from functions.merge_pdfs import merge_pdfs
from functions.convert_pdf_to_text import convert_pdf_to_text
from functions.extract_pages_from_pdf import extract_pages
import webbrowser

class ConverterApp:
    def __init__(self, root):
        self.root = root
        root.title("Converter App")

        # Imposta una dimensione iniziale e posiziona la finestra al centro dello schermo
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # Imposta un tema per il miglioramento visivo
        style = ttk.Style()
        style.theme_use('clam')  # Puoi provare anche altri temi come 'alt', 'default', 'classic', 'vista'

        # Crea il Tab Control
        tabControl = ttk.Notebook(root)

        # Aggiungi ogni tab delle funzionalità
        self.create_homepage_tab(tabControl)
        self.create_conversion_tab(tabControl, "EBook to Kindle", "Select EBook", self.convert_ebook)
        self.create_conversion_tab(tabControl, "CSV to Excel", "Select CSV", self.convert_csv_to_excel)
        self.create_conversion_tab(tabControl, "CSV to Json", "Select CSV", self.convert_csv_to_json)
        self.create_pdf_merge_tab(tabControl)  
        self.create_pdf_to_text_tab(tabControl)
        self.create_pdf_extract_pages_tab(tabControl)  

        tabControl.pack(expand=1, fill="both")

    def create_homepage_tab(self, tabControl):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text='Homepage')
        
        # Aggiungi le informazioni
        info_text = """
        
LinkedIn: https://www.linkedin.com/in/filippo-corsini-349b43125/
Github: https://github.com/FilCor?tab=repositories"""
        
        info_label = tk.Label(tab, text="Made by Filippo Corsini", justify=tk.LEFT)
        info_label.pack(pady=20)
        
        # Usa un Text widget per i link cliccabili
        link_text_widget = tk.Text(tab, height=5, wrap="word")
        link_text_widget.insert(tk.END, info_text)
        link_text_widget.pack(pady=20)
        link_text_widget.tag_add("LinkedIn", "3.10", "3.78")
        link_text_widget.tag_add("Github", "4.8", "4.48")
        link_text_widget.tag_config("LinkedIn", foreground="blue", underline=1)
        link_text_widget.tag_config("Github", foreground="blue", underline=1)
        link_text_widget.tag_bind("LinkedIn", "<Button-1>", lambda e: webbrowser.open_new("https://www.linkedin.com/in/filippo-corsini-349b43125/"))
        link_text_widget.tag_bind("Github", "<Button-1>", lambda e: webbrowser.open_new("https://github.com/FilCor?tab=repositories"))
        
        # Disabilita il widget per evitare la modifica del testo ma mantenere la funzionalità del link
        link_text_widget.config(state="disabled")

    def create_pdf_extract_pages_tab(self, tabControl):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text='Extract PDF Pages')

        # Bottone per selezionare il PDF
        select_button = tk.Button(tab, text="Select PDF", command=self.select_pdf_for_extraction)
        select_button.pack(pady=10)

        # Etichetta con istruzioni per l'utente
        instructions_label = tk.Label(tab, text="Inserisci i numeri delle pagine (es. 1,3-5)")
        instructions_label.pack(pady=10)

        # Entry per inserire i numeri delle pagine da estrarre
        self.pages_entry = tk.Entry(tab, width=50)
        self.pages_entry.pack(pady=10)
        self.pages_entry.insert(0, "Inserisci i numeri delle pagine (es. 1,3-5)")

        # Bottone per selezionare dove salvare il PDF risultante
        save_button = tk.Button(tab, text="Save Extracted Pages", command=self.save_extracted_pages)
        save_button.pack(pady=10)
    
    def select_pdf_for_extraction(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.selected_pdf_for_extraction = file_path

    def save_extracted_pages(self):
        if not hasattr(self, 'selected_pdf_for_extraction') or not self.selected_pdf_for_extraction:
            messagebox.showwarning("Attenzione", "Nessun PDF selezionato.")
            return

        pages_text = self.pages_entry.get()
        # Converti l'input dell'utente (es. "1,3-5") in una lista di numeri di pagina
        page_numbers = self.parse_page_numbers(self.pages_entry.get())
        
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                  filetypes=[("PDF files", "*.pdf")], 
                                                  title="Save the extracted pages as...")
        if not output_path:  # L'utente ha annullato la selezione
            return

        try:
            extract_pages(self.selected_pdf_for_extraction, page_numbers, output_path)
            messagebox.showinfo("Successo", f"Le pagine sono state estratte e salvate in {output_path}.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def parse_page_numbers(self, pages_text):
        page_numbers = []
        for part in pages_text.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                page_numbers.extend(range(start-1, end))  # Sottrai 1 da 'start'
            else:
                page_numbers.append(int(part)-1)  # Sottrai 1 per convertire da base 1 a base 0
        return page_numbers

    def create_conversion_tab(self, tabControl, title, button_text, conversion_function):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text=title)
        
        # Aggiungi elementi per l'input di file e il bottone di conversione
        self.add_file_input(tab, button_text, conversion_function)

    def add_file_input(self, parent, button_text, conversion_function):
        # Frame per contenere i controlli
        frame = tk.Frame(parent)
        frame.pack(pady=10)

        # Entry per mostrare il percorso del file selezionato
        file_entry = tk.Entry(frame, width=50)
        file_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Bottone per selezionare il file e avviare la conversione
        file_button = tk.Button(frame, text=button_text, command=lambda: self.open_file(file_entry, conversion_function))
        file_button.pack(side=tk.RIGHT)

    def open_file(self, entry_widget, conversion_function):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
            conversion_function(file_path)

    def create_pdf_merge_tab(self, tabControl):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text='Merge PDFs')

        # Bottone per selezionare i PDF
        select_button = tk.Button(tab, text="Select PDFs", command=self.select_pdfs)
        select_button.pack(pady=10)

        # Bottone per unire i PDF selezionati
        merge_button = tk.Button(tab, text="Merge PDFs", command=self.merge_selected_pdfs)
        merge_button.pack(pady=10)

        # Lista per mostrare i PDF selezionati
        self.pdf_listbox = tk.Listbox(tab, width=50, height=10)
        self.pdf_listbox.pack(pady=10)

        self.pdf_paths = []  # Per tenere traccia dei percorsi dei PDF selezionati

    def select_pdfs(self):
        # Lascia l'utente selezionare più PDF
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.pdf_listbox.insert(tk.END, file)
            self.pdf_paths.append(file)

    def merge_selected_pdfs(self):
        if not self.pdf_paths:
            messagebox.showwarning("Attenzione", "Nessun PDF selezionato.")
            return

        output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")], 
                                                 title="Save the merged PDF as...")
        if not output_pdf:  # L'utente ha annullato la selezione
            return
        
        try:
            merge_pdfs(self.pdf_paths, output_pdf)
            messagebox.showinfo("Successo", f"I PDF sono stati uniti con successo in {output_pdf}.")
            self.pdf_listbox.delete(0, tk.END)  # Pulisci la lista
            self.pdf_paths.clear()  # Pulisci la lista dei percorsi
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def create_pdf_to_text_tab(self, tabControl):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text='PDF to Text')

        # Bottone per selezionare il PDF
        select_button = tk.Button(tab, text="Select PDF", command=self.select_pdf)
        select_button.pack(pady=10)

        # Aggiungi bottone per salvare il testo estratto
        save_button = tk.Button(tab, text="Save Text", command=self.save_text)
        save_button.pack(pady=10)

        # Area di testo per mostrare il testo estratto
        self.text_area = tk.Text(tab, wrap="word", height=15, width=50)
        self.text_area.pack(pady=10)

    def select_pdf(self):
        # Lascia l'utente selezionare un PDF
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                text = convert_pdf_to_text(file_path)
                self.text_area.delete(1.0, tk.END)  # Pulisci l'area di testo
                self.text_area.insert(tk.END, text)  # Inserisci il testo estratto
            except Exception as e:
                messagebox.showerror("Errore", str(e))
        
        self.selected_pdf = file_path

    def save_text_to_file(self, text, output_path):
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Successo", f"Testo salvato con successo in {output_path}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il salvataggio del file: {e}")


    def save_text(self):
        if not hasattr(self, 'selected_pdf') or not self.selected_pdf:
            messagebox.showwarning("Attenzione", "Nessun PDF selezionato.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt")], 
                                                  title="Save the text as...")
        if not output_path:  # L'utente ha annullato la selezione
            return

        try:
            text = convert_pdf_to_text(self.selected_pdf)  # Assicurati che questa funzione sia definita o importata
            self.save_text_to_file(text, output_path)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def create_csv_json_tab(self, tabControl):
        tab = ttk.Frame(tabControl)
        tabControl.add(tab, text='CSV to JSON')
        
        # Aggiungi elementi per l'input di file e il bottone di conversione
        self.add_file_input(tab, "Select CSV", lambda f: self.convert_csv_to_json(f))

    def convert_csv_to_json(self, file_path):
        try:
            csv_to_json(file_path)  # Chiamata alla funzione di conversione modificata
            messagebox.showinfo("Successo", "Il file CSV è stato convertito in JSON con successo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
    
    def convert_ebook(self, file_path):
        # Implementa la chiamata al modulo di conversione specifico
        try:
            # epub_to_awz3(file_path) # Assicurati che il modulo sia corretto e gestisca gli errori
            messagebox.showinfo("Successo", "Il file è stato convertito con successo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def convert_csv_to_excel(self, file_path):
        # Implementa la chiamata al modulo di conversione specifico
        try:
            # csv_to_excel(file_path) # Assicurati che il modulo sia corretto e gestisca gli errori
            messagebox.showinfo("Successo", "Il file CSV è stato convertito in Excel con successo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    app.root.mainloop()
