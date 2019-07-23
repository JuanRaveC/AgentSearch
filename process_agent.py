from glob import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml_processing import create_xml_file
from print_results_manager import print_all_results
import time
from queue import Queue
from process_retrieved_information import process_file_for_search, process_file_for_batch
from pathlib import Path

class ProcessAgent():

    self_queue = Queue()

    @staticmethod
    def work():
        while True:
            #validar la cola
            if ProcessAgent.self_queue.empty():
                #obtener archivos a procesar
                processed_response = ''
                # obtener archivos a procesar
                for file_name in Path(ProcessAgent.folder_name).glob('**/*.html'):
                    #print(file_name)
                    if 'TDA' in str(file_name):
                        processed_response = process_file_for_batch(str(file_name), 'TDA')
                if not processed_response:
                    print('No existen archivos para procesar!!')
                    time.sleep(5)
            else:
                key_word = ProcessAgent.self_queue.get()
                print("cola del agente PROCESADOR tiene {}".format(key_word))
                time.sleep(2)
                #procesar archivos en caso de busqueda a demanda
                poli_file_name = Path(ProcessAgent.folder_name+"/"+key_word+"-POLIJIC.html")
                process_result_poli = process_file_for_search(poli_file_name, key_word, 'POLIJIC')
                #process_result_poli = process_file_for_search(key_word+'-POLIJIC.html', key_word, 'POLIJIC')
                tda_file_name = Path(ProcessAgent.folder_name+"/"+key_word+"-TDA.html") 
                process_result_tda = process_file_for_search(tda_file_name, key_word, 'TDA')
                #process_result_col = process_file_for_search(key_word+'-COLMA.html')
                #print_results(process_result_poli, process_result_tda, process_result_col)
                #print_results(Path("base_response.html"), process_result_tda, key_word)
                print_all_results(Path("base_response.html"), key_word,process_result_tda, process_result_poli, "hola colmalievers 100")
                create_xml_file(process_result_poli+process_result_tda, key_word)


    def __init__(self, self_queue, index_queue, join_queue, folder_name):
        ProcessAgent.self_queue = self_queue
        ProcessAgent.index_queue = index_queue
        ProcessAgent.join_queue = join_queue
        ProcessAgent.folder_name = folder_name