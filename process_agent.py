from glob import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml_processing import create_xml_file
from print_results_manager import print_results
import time
from queue import Queue

class ProcessAgent():

    self_queue = Queue()

    @staticmethod
    def process_file(file_name):
        processed_results = []
        try:
            #uso de beutifulsoup para realizar el analisis
            soup = BeautifulSoup(open(file_name), "html.parser")
            #recorrer el resultado de la funcion find() de beautifulsoup
            for titulo, autor, tipo, biblioteca, descripcion in soup.find('span', {'class': 'titulo'}, {'class': 'autor'}, {'class': 'tipo'}, {'class': 'biblioteca'}, {'class': 'descripcion'}):
                processed_results.append('Titulo: '+titulo)
                processed_results.append('Autor: '+autor)
                processed_results.append('Tipo: '+tipo)
                processed_results.append('Biblioteca: '+biblioteca)
                processed_results.append('Descripcion: '+descripcion)
            #creación de xml
            create_xml_file(processed_results)
        except Exception as error:
            print(error)
        finally:
            return processed_results

    @staticmethod
    def work():
        while True:
            #validar la cola
            if not ProcessAgent.self_queue.empty():
                key_word = ProcessAgent.self_queue.get()
                #obtener archivos a procesar
                file_list = glob(ProcessAgent.folder_name+'/*.html')
                if file_list is not None:
                    for file in file_list:
                        #procesar cada archivo encontrado
                        ProcessAgent.process_file(file)
                else:
                    print('No existen archivos a procesar')
                    time.sleep(5)
            else:
                #procesar archivos en caso de busqueda a demanda
                process_result_poli = ProcessAgent.process_file(key_word+'-POLIJIC.html')
                process_result_tda = ProcessAgent.process_file(key_word+'-TDA.html')
                process_result_col = ProcessAgent.process_file(key_word+'-COLMA.html')
                
                print_results(process_result_poli, process_result_tda, process_result_col)

    def __init__(self, self_queue, index_queue, join_queue, folder_name):
        ProcessAgent.self_queue = self_queue
        ProcessAgent.index_queue = index_queue
        ProcessAgent.join_queue = join_queue
        ProcessAgent.folder_name = folder_name
        ProcessAgent.work()