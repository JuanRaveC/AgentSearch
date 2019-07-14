import time
from db_manager import *
from queue import Queue

class IndexAgent():

    @staticmethod
    def work():
        while True:
            if not IndexAgent.self_queue.empty():
                try:
                    key_word = IndexAgent.self_queue.get()
                    print("palabra obtenida de la cola: " + key_word)
                    IndexAgent.self_queue.task_done()
                    #realizar ordenamiento de la BD
                    order_query = "alter table agentdb.historial order by palabra_clave asc"
                    if not generic_db_opperation(order_query):
                        print('error en proceso de indexar')
                except Exception as error:
                    print(error)
            else:
                print("No hay nada en la cola!!")
                time.sleep(5)
                #query de insercion a la bd de temas
                insert_theme_query = "inset into agentdb.tema(tema) values('{}')"
                #buscar registros que tengan mas de un mes de antiguedad
                registries_to_update_query = "select * from agentdb.historial where fecha < (CURDATE()- INTERVAL 30 DAY)"
                registry_list = generic_query(registries_to_update_query)
                if registry_list is not None:
                    for registry in registry_list:
                        print(registry)
                #        if not generic_insert(insert_theme_query.format(registry)):
                #            print('error insertando tema')
                else:
                    print('No existen archivos a procesar')
                    time.sleep(5)

    def __init__(self, self_queue, join_queue, process_queue):
        print("Estoy en el agente indexador!")
        IndexAgent.self_queue = self_queue
        IndexAgent.index_queue = join_queue
        IndexAgent.join_queue = process_queue