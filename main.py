from crawler import Crawler
from utils import *

FOLDER_NAME = 'HTML'

if __name__ == '__main__':
    print('inicia el programa!')
    print('Creando directorio: '+ FOLDER_NAME)
    create_data_dir(FOLDER_NAME)
    print('Creando Crawler')
    Crawler(FOLDER_NAME)