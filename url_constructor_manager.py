from db_manager import *

base_url_list_query = "select url, institucion from agentdb.url_base"

def construct_url(base_url_list, key_word, key_word_id):
    insert_statement = "insert into url(url, id_tema, institucion, crawled_ind) values('{}',{},'{}',0)"
    #iteracion en cada una de las url bases
    for url in base_url_list:
        #procesamiento de url
        processed_url = url['url'].format(key_word)
        #validacion del inser
        if(generic_insert(insert_statement.format(processed_url,key_word_id,url['institucion']))):
            print('insert correcto')
            return True
        else:
            print('Error insertando direccion procesada')
            return False
    
#agente constructor
def url_constructor():
    themes_query = "select tema, id_tema from agentdb.tema where id_xml is null"
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
        return True

def construct_url_for_search(base_url_list, key_word):
    #iteracion en cada una de las url bases
    processed_list = []
    for url in base_url_list:
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

    