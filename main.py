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


class Application:
    def __init__(self, master):

        # 1: crear un builder
        self.builder = builder = pygubu.Builder()
        # 2: cargar archiv ui
        builder.add_from_file('C:/Users/USUARIO/Documents/mainframe.ui')
        # 3: Crear widgets
        self.mainwindow = builder.get_object('Frame_1', master)


if __name__ == '__main__':
    print('Creando directorio: ' + FOLDER_NAME)
    create_data_dir(FOLDER_NAME)
    # Inicializar los agentes

    # inicializando agentes
    #creación de colas
    process_agent_queue = Queue()
    index_agent_queue = Queue()
    join_agent_queue = Queue()

    # agente integrador
    join_agent = threading.Thread(target=JoinAgent(join_agent_queue, index_agent_queue, process_agent_queue))
    join_agent.daemon = True
    join_agent.start()

    # agente procesador
    process_agent = threading.Thread(target=ProcessAgent(process_agent_queue, index_agent_queue, join_agent_queue, FOLDER_NAME))
    process_agent.daemon = True
    process_agent.start()

    # agente indexador
    index_agent = threading.Thread(target=IndexAgent(index_agent_queue, join_agent_queue, process_agent_queue))
    index_agent.daemon = True
    index_agent.start()

    # Creando crawler principal
    crawler = threading.Thread(target=Crawler(FOLDER_NAME))
    index_agent.daemon = True
    index_agent.start()

    # iniciar la pantalla principal
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
