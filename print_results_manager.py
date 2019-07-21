import codecs
import webbrowser
from utils import create_data_files
from pathlib import Path

FOLDER_NAME = 'HTML'
FILE_LASTNAME = "-respuesta"
FILE_EXTENSION = ".html"
SLASH = "/"

def print_results(file_name, data, key_word):
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