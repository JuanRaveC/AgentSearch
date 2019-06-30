from db_connection import db_connection
from urllib.request import urlopen
# from link_finder import LinkFinder
from utils import *


class Crawler:
    # Creacion de objeto de conexion a la db
    conn = db_connection()
    # crea cursor de tipo dict
    cursor = conn.cursor(dictionary=True)
    # constantes
    QUERY = 'select * from agentdb.url where crawled_ind = 0 limit 1'
    UPDATE = 'update agentdb.url set crawled_ind = %s where id_url = %s'
    THEME_NAME = 'select tema from agentdb.tema where id_tema = 215454'
    folder_name = ''

    def __init__(self, folder_name):
        Crawler.folder_name = folder_name
        Crawler.crawl_page('crawler_init')

    # obtener url de la tabla para proceder a hacer el crawling
    @staticmethod
    def fetch_url_info():
        try:
            Crawler.cursor.execute(Crawler.QUERY)
            # row = cursor.fetchone()
            for row in Crawler.cursor:
                return row['id_url'], row['url'], row['id_tema']
        except Exception as error:
            print(error)
            print('Error al consultar la url a Crawlear')
            return '',''

    #hace el update en el registro/url que se consultó para marcar como visitada
    @staticmethod
    def update_url(indicator, url_id):
        data = (indicator, url_id)
        try:
            Crawler.cursor.execute(Crawler.UPDATE, data)
        except Exception as error:
            print(error)
            print('Error al actualizar la url')
        finally:
            cursor.close()
            conn.close()
        
    @staticmethod
    def get_theme(theme_id):
        try:
            Crawler.cursor.execute(Crawler.THEME_NAME)
            for row in Crawler.cursor:
                return row['tema']
        except Exception as error:
            print(error)
            print('Error al consultar el id del tema')
            return ''

    # obtiene url a crawlear y una vez termina, guarda archivo con informacion encontrada
    @staticmethod
    def crawl_page(thread_name):
        html_string = ''
        url_info = Crawler.fetch_url_info()
        #print(url_info)
        url_to_crawl = url_info[1]
        #print(url_to_crawl)
        url_id = url_info[0]
        print(url_id)
        theme_id = url_info[2]
        print(theme_id)
        print(thread_name + ' Crawling ')#+ url_to_crawl)
        if url_info is not None:
            try:
                response = urlopen(url_to_crawl)
                if 'text/html' in response.getheader('Content-Type'):
                    html_bytes = response.read()
                    html_string = html_bytes.decode("utf-8")
                    create_data_files(Crawler.folder_name, Crawler.get_theme(theme_id), html_string)
                    #Crawler.update_url(1,url_id)
            except Exception as e:
                print(str(e))
                #Crawler.update_url(0, url_id)
        else:
            print('Error al obtener url')