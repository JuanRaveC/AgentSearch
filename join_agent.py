from queue import Queue
from threading import Thread
from url_constructor_manager import url_constructor, url_construct_for_search
from crawler import Crawler
import time

class JoinAgent():

    @staticmethod
    def work():
        while True:
            key_word = JoinAgent.self_queue.get()
            if key_word:
                if not url_constructor():
                    time.sleep(5)
            else:
                url_list = url_construct_for_search(key_word)
                if url_list is not None:
                    for url in url_list:
                        Crawler.crawl_page_for_search(url, key_word)

                    #se comunica con el agente de procesamiento
                    JoinAgent.process_queue.put(key_word)
                    #desencola
                    JoinAgent.self_queue.task_done()

    def __init__(self, self_queue, index_queue, process_queue):
        JoinAgent.self_queue = self_queue
        JoinAgent.index_queue = index_queue
        JoinAgent.process_queue = process_queue
        JoinAgent.work()
