from glob import glob
from bs4 import BeautifulSoup
from print_results_manager import print_results_tda, print_results_polijic
import time
from queue import Queue
from pathlib import Path
import codecs
import os


def process_tda_file(soup):
    '''
    Titulo:  
    Autor: 
    Tipo: 
    Biblioteca: 
    Descripcion:
    '''
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
    '''
    Titulo:  
    Autor: 
    Tipo: 
    Biblioteca: 
    Descripcion:
    '''
    response = ''
    number_of_registries = 0
    for tr in soup.findAll('tr', {'valign': 'baseline'}):
        response += '------------------------------------------------------------------------------------------------------------\n'
        tr_title = tr.find('script').text
        tr_title = tr_title.split('/')[0]
        response += 'Titulo: ' + \
            tr_title[tr_title.find("'") + 1:tr_title.find(";") - 1] + '\n'
        tr_author = tr.find('td', {'width': '20%'})
        response += 'Autor: ' + tr_author.text + '\n'
        tr_type = tr.find('td', {'width': '5%'})
        response += 'Tipo: ' + tr_type.text + '\n'
        tr_library = 'Biblioteca: Tomás Carrasquilla'
        response += tr_library + '\n'
        tr_description = tr.find(
            'script').next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.string
        response += 'Descripcion: ' + tr_description + '\n'
        number_of_registries += 1
    response += 'Cantidad de registros: ' + str(number_of_registries) + '\n'
    return response


def process_file_for_search(file_name, key_word, institution):
    if key_word in str(file_name):
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                if 'TDA' in institution:
                    response =  process_tda_file(soup)
                elif 'POLIJIC' in institution:
                    response = process_polijic_file(soup)
                else:
                    pass
            try:
                Path.unlink(file_name)
                pass
            except OSError as error:
                print("Error: {} - {}.".format(error.filename, error.strerror))

            return response
        except Exception as error:
            print(error)
    else:
        pass


def process_file_for_batch(file_name, institution):
    try:
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            if 'TDA' in institution:
                return process_tda_file(soup)
            elif 'POLIJIC' in institution:
                return process_polijic_file(soup)
            else:
                pass
    except Exception as error:
        print(error)


#tda_data = process_file_for_search(
#    Path("HTML/java-POLIJIC.html"), 'java', 'POLIJIC')
#print_results_polijic(Path("base_response.html"), tda_data, 'java')
