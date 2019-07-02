from db_connection import db_connection
from urllib.request import urlopen
from utils import *
from bs4 import BeautifulSoup


class Crawler:
    # Creacion de objeto de conexion a la db
    conn = db_connection()
    # crea cursor de tipo dict
    cursor = conn.cursor(dictionary=True)
    # constantes
    URL_QUERY = 'select * from agentdb.url where crawled_ind = 0 limit 1'
    URL_UPDATE = 'update agentdb.url set crawled_ind = {} where id_url = {}'
    THEME_INFORMATION = 'select tema from agentdb.tema where id_tema = {}'
    folder_name = ''

    def __init__(self, folder_name):
        Crawler.folder_name = folder_name
        Crawler.crawl_page('crawler_init')

    # obtener url de la tabla para proceder a hacer el crawling
    @staticmethod
    def fetch_url_info():
        try:
            Crawler.cursor.execute(Crawler.URL_QUERY)
            # row = cursor.fetchone()
            for row in Crawler.cursor:
                return row['id_url'], row['url'], row['id_tema'], row['institucion']
        except Exception as error:
            print(error)
            print('Error al consultar la url a Crawlear')
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
            print(error)
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
            print('Error al consultar el id del tema')
            return '', ''

    # obtiene url a crawlear y una vez termina, guarda archivo con informacion encontrada
    @staticmethod
    def crawl_page(thread_name):
        html_string = ''
        url_info = Crawler.fetch_url_info()
        if url_info is not None:
            url_to_crawl = url_info[1]
            url_id = url_info[0]
            theme_id = url_info[2]
            url_institution = url_info[3]
            print(thread_name + ' Crawling ')
            try:
                # se hace la peticion GET a la url
                response = urlopen(url_to_crawl)
                # valida si la respuesta es de tipo texto en el header content-type
                if 'text/html' in response.getheader('Content-Type'):
                    # obtiene el html en una variable de bytes
                    html_bytes = response.read()
                    # decodifica los bytes con el decode utf-8 del parser
                    print(response.headers.get_content_charset())
                    html_string = html_bytes.decode('cp1252')
                    # crea archivo con la respuesta en el folder
                    file_name = Crawler.get_theme(theme_id)+'-'+url_institution
                    print(file_name)
                    create_data_files(Crawler.folder_name,
                                      file_name, html_string)
                    # marca la url visitada
                    # Crawler.update_url(1,url_id)
            except Exception as e:
                print(str(e))
                Crawler.update_url(0, url_id)
        else:
            print('Error al obtener url')


#import requests
#from bs4 import BeautifulSoup

#url='https://campus.tdea.edu.co/bivi/busquedaExterna.do?blnExterna=1&strAccion=busquedaBasica&strOpcionesBusqueda=ITEM.STRTITULO&strBusqueda=ciencia&idColeccion=-1'
#webpage=requests.get(url, verify=False)
#soup= BeautifulSoup(webpage.content, 'html.parser')
#content=str(webpage.content, 'windows-1252')
#print(content)