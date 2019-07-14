from crawler import Crawler
from utils import *
from index_agent import IndexAgent
from process_agent import ProcessAgent
from join_agent import JoinAgent
from queue import Queue
import threading
import tkinter as tk  # python 3
import pygubu

FOLDER_NAME = 'HTML'
#creación de colas
process_agent_queue = Queue()
index_agent_queue = Queue()
join_agent_queue = Queue()

class Application:
    def __init__(self, master):

        # 1: crear un builder
        self.builder = builder = pygubu.Builder()
        # 2: cargar archiv ui
        builder.add_from_file('C:/Users/USUARIO/Documents/mainframe.ui')
        # 3: Crear widgets
        self.mainwindow = builder.get_object('Frame_1', master)
        #continuar con el hilo de ejecución de la UI
        builder.connect_callbacks(self)

    #obtener informacion del campo de texto
    def retrieve_input(self):
        text_input_object = self.builder.get_variable('search_input')
        keyword_input = text_input_object.get()
        #envia a la cola
        #index_agent_queue.put(keyword_input) #no es el agente que debe recibir, solo estoy probando
        join_agent_queue.put(keyword_input)
        text_input_object.set(' ')


    #evento del boton buscar
    def search_on_click(self):
        Application.retrieve_input(self)


if __name__ == '__main__':
    print('Creando directorio: ' + FOLDER_NAME)
    create_data_dir(FOLDER_NAME)
    flag = True
    # Inicializar los agentes

    # inicializando agentes

    # Creando crawler principal
    #crawler = threading.Thread(target=Crawler(FOLDER_NAME))
    #crawler.daemon = True
    #crawler.start()
    #singleton de inicialización
    if flag:
        #Agente integrador
        join_agent_instance = JoinAgent(join_agent_queue, index_agent_queue, process_agent_queue, FOLDER_NAME)
        join_agent_thread = threading.Thread(target=join_agent_instance.work)
        join_agent_thread.daemon = True
        join_agent_thread.start()  
        print("Volvi al main!")

        # agente indexador
        #index_agent_instance = IndexAgent(index_agent_queue, join_agent_queue, process_agent_queue)
        #index_agent_thread = threading.Thread(target=index_agent_instance.work)
        #index_agent_thread.daemon = True
        #index_agent_thread.start()
        #index_agent_queue.put("Hola agente")
        #print("Volvi al main!")

        #agente procesador
        '''process_agent_instance = ProcessAgent(process_agent_queue, index_agent_queue, join_agent_queue, FOLDER_NAME)
        process_agent_thread = threading.Thread(target=process_agent_instance.work)
        process_agent_thread.daemon = True
        process_agent_thread.start()
        print("Volvi al main!")
        '''
        #no volver a inicializar mas
        flag = False
    
    # iniciar la pantalla principal
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
