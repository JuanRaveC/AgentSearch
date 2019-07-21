from glob import glob
from bs4 import BeautifulSoup
from print_results_manager import print_results
import time
from queue import Queue
from pathlib import Path
import codecs
import os


def process_tda_file(soup):
    response = ''
    quantity = 0
    for td in soup.find_all('td'):
        if td.a:
            href = td.a.get('href')
            value = td.a.text
            if href is not None:
                if 'TITULO' in href:
                    response += '------------------------------------------------------------------------------------------------------------' + '\n'
                    key = 'Titulo: '
                    quantity += 1
                    response += (key + value + '\n')
                elif 'NOMBRE' in href:
                    key = 'Autor: '
                    response += (key + value + '\n')
                    response += 'Tipo: libro' + '\n'
            else: 
                pass
        else:
            value = td.text
            if 'Biblioteca' in value:
                key = 'Biblioteca: Humberto Saldarriaga Carmona' + '\n'
                response += key
            elif 'LIBRE' in value:
                key = 'Descripcion: '
                response += key + value + '\n'
    response += ('Cantidad de registros: ' + str(quantity) + '\n')
    return response

def process_polijic_file(soup):
    pass

def process_file_for_search(file_name, key_word, institution):
    if key_word in str(file_name):
        try:
            #print(file_name)
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(),"html.parser")
                if 'TDA' in institution:
                    response =  process_tda_file(soup)
                #elif 'POLIJIC' in institution:
                #    return process_polijic_file(soup)
            try:
                #Path.unlink(file_name)
                pass
            except OSError as error:  
                print ("Error: {} - {}.".format(error.filename, error.strerror))
            
            return response
        except Exception as error:
            print(error)
    else:
        pass    

def process_file_for_batch(file_name, institution):
    try:
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(),"html.parser")
            if 'TDA' in institution:
                return process_tda_file(soup)
            #elif 'POLIJIC' in institution:
            #    return process_polijic_file(soup)
            else:
                pass
    except Exception as error:
        print(error)
    

#tda_data = process_file_for_search(Path("HTML/java-TDA.html"), 'java', 'TDA')
#print_results(Path("base_response.html"), tda_data, 'java')