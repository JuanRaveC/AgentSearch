from db_connection import db_connection
from urllib.request import urlopen
from utils import create_data_files
from bs4 import BeautifulSoup
import requests
import time


class Crawler:
    # Creacion de objeto de conexion a la db
    conn = db_connection()
    # crea cursor de tipo dict
    cursor = conn.cursor(dictionary=True)
    # constantes
    URL_QUERY = 'select * from agentdb.url where crawled_ind = 0 limit 1'
    URL_UPDATE = 'update agentdb.url set crawled_ind = {} where id_url = {}'
    THEME_INFORMATION = 'select tema from agentdb.tema where id_tema = {}'
    folder_name = 'HTML'

    def __init__(self, folder_name):
        Crawler.folder_name = folder_name
        Crawler.crawl_page('crawler_init')

    # obtener url de la tabla para proceder a hacer el crawling
    @staticmethod
    def fetch_url_info():
        try:
            Crawler.cursor.execute(Crawler.URL_QUERY)
            for row in Crawler.cursor:
                return row['id_url'], row['url'], row['id_tema'], row['institucion']
        except Exception as error:
            print('NO hay URLs a buscar')
            return '', ''

    # hace el update en el registro/url que se consultó para marcar como visitada
    @staticmethod
    def update_url(indicator, url_id):
        update_query = Crawler.URL_UPDATE.format(indicator, url_id)
        print(update_query)
        try:
            Crawler.cursor.execute(update_query)
            Crawler.conn.commit()
        except Exception as error:
            print('Error al actualizar la url')
        finally:
            Crawler.cursor.close()
            Crawler.conn.close()

    # metodo para obtener el tema de la url que se visita
    @staticmethod
    def get_theme(theme_id):
        query = Crawler.THEME_INFORMATION.format(theme_id)
        try:
            Crawler.cursor.execute(query)
            for row in Crawler.cursor:
                return row['tema']
        except Exception as error:
            print(error)
            print('No hay temas a buscar')
            return '', ''

    # obtiene url a buscar y una vez termina, guarda archivo con informacion encontrada
    @staticmethod
    def crawl_page(thread_name):
        url_info = Crawler.fetch_url_info()
        if url_info is not None:
            if url_info[0] and url_info[1]:
                url_to_crawl = url_info[1]
                url_id = url_info[0]
                theme_id = url_info[2]
                url_institution = url_info[3]
                try:
                    str_theme = Crawler.get_theme(theme_id)
                    Crawler.crawl_page_for_search(url_to_crawl,str_theme, Crawler.folder_name)
                    Crawler.update_url(1, url_id)
                except Exception as e:
                    print(str(e))
                    Crawler.update_url(0, url_id)
            else:
                pass
        else:
            print('Error al obtener url')

    @staticmethod
    def crawl_page_for_search(url_to_crawl, key_word, folder_name):
        try:
            #validar a que institucion pertenece la url a buscar
            if 'aleph' in str(url_to_crawl):
                url_institution = 'POLIJIC'
                # se hace la peticion GET a la url
                webpage = requests.get(url_to_crawl, verify=False)
            elif 'tdea' in str(url_to_crawl):
                url_institution = 'TDA'
                # se hace la peticion GET a la url
                webpage = requests.post(url_to_crawl, verify=False)
            else:
                url_institution = 'COLMA'
                # se hace la peticion GET a la url
                webpage = requests.post(url_to_crawl, verify=False)

            content = webpage.text
            file_name = key_word+'-'+url_institution
            create_data_files(folder_name, file_name, content)
        except Exception as e:
                print(str(e))

    @staticmethod
    def work():

        while True:
            Crawler.crawl_page('crawler_init')
            time.sleep(5)