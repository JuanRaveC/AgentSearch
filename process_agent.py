from glob import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml_processing import create_xml_file
import main
import time

class ProcessAgent():

    @staticmethod
    def process_file(file_name):
        processed_results = []
        soup = BeautifulSoup(open(file_name), "html.parser")
        for titulo, autor, tipo, biblioteca, descripcion  in soup.find('span', {'class' : 'titulo'}, {'class' : 'autor'}, {'class' : 'tipo'}, {'class' : 'biblioteca'}, {'class' : 'descripcion'}):
            processed_results.append('Titulo: '+titulo)
            processed_results.append('Autor: '+autor)
            processed_results.append('Tipo: '+tipo)
            processed_results.append('Biblioteca: '+biblioteca)
            processed_results.append('Descripcion: '+descripcion)
            processed_results.append('---------------------------------------')

        create_xml_file(processed_results)
        print_results(processed_results)

    @staticmethod
    def work():
        while True:
            key_word = ProcessAgent.self_queue.get()
            if key_word:
                file_list = glob(ProcessAgent.folder_name+'/*.html')
                if file_list is not None:
                    for file in file_list:
                        ProcessAgent.process_file(file)
                else:
                    print('No existen archivos a procesar')
                    time.sleep(5)
            else:
                ProcessAgent.process_file(key_word+'-POLIJIC.html')
                ProcessAgent.process_file(key_word+'-TDA.html')
                ProcessAgent.process_file(key_word+'-COLMA.html')

    def __init__(self, self_queue, index_queue, join_queue, folder_name):
        ProcessAgent.self_queue = self_queue
        ProcessAgent.index_queue = index_queue
        ProcessAgent.join_queue = join_queue
        ProcessAgent.folder_name = folder_name
        ProcessAgent.work()