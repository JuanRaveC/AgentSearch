from queue import Queue
from threading import Thread
from url_constructor_manager import url_constructor, url_constructor_for_search
from crawler import Crawler
import time

class JoinAgent():

    @staticmethod
    def work():
        while True:
            #obtiene palabra de la cola
            key_word = JoinAgent.self_queue.get()
            #sino hay palbra en la cola, se hace procesamiento de construccion de urls para temas pendientes
            if not key_word:
                if not url_constructor():
                    #sino encuentra urls para contruir en proceso batch, duerme el proceso 5segundos
                    time.sleep(5)
            else:
                #se obtiene lista de urls a buscar deacuerdo a palabra encontrada en la cola
                url_list = url_constructor_for_search(key_word)
                if url_list is not None:
                    for url in url_list:
                        #se hace crawling por cada url constuida
                        Crawler.crawl_page_for_search(url, key_word)

                    #se comunica con el agente de procesamiento
                    JoinAgent.process_queue.put(key_word)
                    #desencola el mensaje para indicar que ya termino la obtencion de informacion
                    JoinAgent.self_queue.task_done()

    def __init__(self, self_queue, index_queue, process_queue):
        JoinAgent.self_queue = self_queue
        JoinAgent.index_queue = index_queue
        JoinAgent.process_queue = process_queue
        JoinAgent.work()
