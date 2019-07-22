import codecs
import webbrowser
from utils import create_data_files
from pathlib import Path

FOLDER_NAME = 'HTML'
FILE_LASTNAME = "-respuesta"
FILE_EXTENSION = ".html"
SLASH = "/"


def print_all_results(file_name, key_word, tda_data, poli_data, colma_data):
    #apertura de archivo base
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        html = f.read()
        if tda_data:
            tda_number_of_records = tda_data[-3:]
            html = html.replace("tda_data", tda_data)
            html = html.replace("tda_number_of_records", tda_number_of_records)
        else:
            html = html.replace("tda_data", "No hay registros")
            html = html.replace("tda_number_of_records", "0")
        if poli_data:
            polijic_number_of_records = poli_data[-3:]
            html = html.replace("poli_data", poli_data)
            html = html.replace("polijic_number_of_records", polijic_number_of_records)
        else:
            html = html.replace("poli_data", "No hay registros")
            html = html.replace("polijic_number_of_records", "0")
        if colma_data:
            colma_number_of_records = colma_data[-3:]
            html = html.replace("colma_data", colma_data)
            html = html.replace("colma_number_of_records", colma_number_of_records)
        else:
            html = html.replace("colma_data", "No hay registros")
            html = html.replace("colma_number_of_records", "0")
    #nombre del archivo
    file_name = Path(FOLDER_NAME + SLASH + key_word + FILE_LASTNAME + FILE_EXTENSION)
    if file_name.exists():
        try:
            Path.unlink(file_name)
            pass
        except OSError as error:  
            print ("Error: {} - {}.".format(error.filename, error.strerror))
    else:
        create_data_files(FOLDER_NAME, key_word + FILE_LASTNAME, html)
    
    webbrowser.open(str(file_name), new = 1, autoraise = True)

def print_results_tda(file_name, data, key_word):
    tda_number_of_records = data[-3:]
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        html = f.read().replace("tda_data", data)
        html = html.replace("tda_number_of_records", tda_number_of_records)
    #nombre del archivo
    file_name = Path(FOLDER_NAME + SLASH + key_word + FILE_LASTNAME + FILE_EXTENSION)
    if file_name.exists():
        try:
            Path.unlink(file_name)
            pass
        except OSError as error:  
            print ("Error: {} - {}.".format(error.filename, error.strerror))
    else:
        create_data_files(FOLDER_NAME, key_word + FILE_LASTNAME, html)
    
    webbrowser.open(str(file_name), new = 1, autoraise = True)

def print_results_polijic(file_name, data, key_word):
    polijic_number_of_records = data[-3:]
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        html = f.read().replace("poli_data", data)
        html = html.replace("polijic_number_of_records", polijic_number_of_records)
    #nombre del archivo
    file_name = Path(FOLDER_NAME + SLASH + key_word + FILE_LASTNAME + FILE_EXTENSION)
    if file_name.exists():
        try:
            Path.unlink(file_name)
            pass
        except OSError as error:  
            print ("Error: {} - {}.".format(error.filename, error.strerror))
    else:
        create_data_files(FOLDER_NAME, key_word + FILE_LASTNAME, html)
    
    webbrowser.open(str(file_name), new = 1, autoraise = True)