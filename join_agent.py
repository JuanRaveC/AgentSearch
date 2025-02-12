from queue import Queue
from threading import Thread
from url_constructor_manager import url_constructor, url_constructor_for_search
from crawler import Crawler
from process_agent import ProcessAgent
from db_manager import generic_query
import time
import webbrowser


class JoinAgent():

    @staticmethod
    def work():
        while True:
            #sino hay palbra en la cola, se hace procesamiento de construccion de urls para temas pendientes
            if JoinAgent.self_queue.empty():
                print("cola del agente INTEGRADOR vacia")
                if not url_constructor():
                    #sino encuentra urls para contruir en proceso batch, duerme el proceso 5segundos
                    time.sleep(5)
            else:
                #obtiene palabra de la cola
                key_word = JoinAgent.self_queue.get()
                existance_query = 'select * from agentdb.historial where palabra_clave like "%{}%"'
                if generic_query(existance_query.format(key_word)):
                    print('encontré en la DB la informacion para: ' + key_word)
                    file_name = key_word + '-procesado.html'
                    webbrowser.open(str(file_name), new = 1, autoraise = True)
                else:
                    print("cola del agente INTEGRADOR tiene {}".format(key_word))
                    #se obtiene lista de urls a buscar deacuerdo a palabra encontrada en la cola
                    url_list = url_constructor_for_search(key_word)
                    if url_list is not None:
                        for url in url_list:
                            #se hace crawling por cada url constuida
                            Crawler.crawl_page_for_search(url, key_word, JoinAgent.FOLDER_NAME)

                        #se comunica con el agente de procesamiento
                        ProcessAgent.self_queue.put(key_word)
                        #desencola el mensaje para indicar que ya termino la obtencion de informacion
                        JoinAgent.self_queue.task_done()

    def __init__(self, self_queue, index_queue, process_queue, FOLDER_NAME):
        JoinAgent.self_queue = self_queue
        JoinAgent.index_queue = index_queue
        JoinAgent.process_queue = process_queue
        JoinAgent.FOLDER_NAME = FOLDER_NAME
