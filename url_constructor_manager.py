from db_manager import *
from bs4 import BeautifulSoup
import requests

#QUERYS BASE GENERICOS
base_url_list_query = "select url, institucion from agentdb.url_base"

#PARAMETROS
#PARAMETROS PARA EL POLIJIC
PARM_JIC = '?func=find-b&request={}&find_code=WRD&adjacent=N&x=53&y=9&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5='

def custom_url_constructor_for_polijic(url_base):
    final_url = ''
    webpage = requests.get(url_base, verify=False)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    for meta in soup.find_all('meta'):
        str_meta = str(meta)
        if 'URL' in str_meta:
            final_url = str_meta.split(';')[1]
            final_url = final_url[5:-36]
            break       
    return final_url + PARM_JIC

def construct_url(base_url_list, key_word, key_word_id):
    insert_statement = "insert into url(url, id_tema, institucion, crawled_ind) values('{}',{},'{}',0)"
    update_statement = "update agentdb.tema set tema_ind = 1 where id_tema = {}"
    #iteracion en cada una de las url bases
    for url in base_url_list:
        #procesamiento de url
        if url['institucion'] == 'POLIJIC':
            processed_url = custom_url_constructor_for_polijic(url['url'])
            processed_url = processed_url.format(key_word)
            print(processed_url)
        else:
            processed_url = url['url'].format(key_word)
        #validacion del insert
        if(generic_insert(insert_statement.format(processed_url,key_word_id,url['institucion']))):
            generic_db_opperation(update_statement.format(key_word_id))
            return True
        else:
            print('Error insertando direccion procesada')
            return False
    
#agente constructor
def url_constructor():
    themes_query = "select tema, id_tema from agentdb.tema where tema_ind = 0"
    #obtener lista de temas a buscar
    themes_list = generic_query(themes_query)
    #obtener lista de urls base
    base_url_list = generic_query(base_url_list_query)
    #validar si alguna de las dos listas esta vacia
    if themes_list and base_url_list is not None:
        for theme in themes_list:
            if (construct_url(base_url_list, theme['tema'], theme['id_tema'])):
                return True
            else:
                return False
    else:
        print('listas vacias')
        return False

def construct_url_for_search(base_url_list, key_word):
    #iteracion en cada una de las url bases
    processed_list = []
    for url in base_url_list:
        #procesamiento de url
        if url['institucion'] == 'POLIJIC':
            processed_url = custom_url_constructor_for_polijic(url['url'])
            #procesamiento de url. Setea la palabra en la url
            processed_url = processed_url.format(key_word)
        else:
            #procesamiento de url. Setea la palabra en la url
            processed_url = url['url'].format(key_word)
        #acumula las urls procesadas
        processed_list.append(processed_url)
    #retorna la lista de urls finales
    return processed_list

def url_constructor_for_search(key_word):
    #obtener lista de urls base
    base_url_list = generic_query(base_url_list_query)
    processed_list = ''
    #validar si la lista esta vacia
    if base_url_list is not None:
        #envia la lista de urls base y la palabra clave para construir url final
        processed_list = construct_url_for_search(base_url_list, key_word)
    else:
        print('listas vacias')
    #se retorna la lista de urls procesadas
    return processed_list