from db_connection import db_connection

# Creacion de objeto de conexion a la db
conn = db_connection()
# crea cursor de tipo dict
cursor = conn.cursor(dictionary=True)

#funcion de consulta generica, retorna una lista
def generic_query(query):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as error:
        print(error)
        print('Error al realizar la consulta '+ query)
        return None

def generic_insert(insert):
    try:
        cursor.execute(insert)
        conn.commit()
        return 1
    except Exception as error:
        print(error)
        print('Error insertando registro '+ insert)
        return 0

def construct_url(base_url_list, key_word, key_word_id):
    insert_statement = "insert into url(url, id_tema, institucion, crawled_ind) values('{}',{},'{}',0)"
    #iteracion en cada una de las url bases
    for url in base_url_list:
        #procesamiento de url
        processed_url = url['url'].format(key_word)
        #validacion del inser
        if(generic_insert(insert_statement.format(processed_url,key_word_id,url['institucion']))):
            print('insert correcto')
        else:
            print('Error insertando direccion procesada')



    
#agente constructor
def constructor_agent():
    base_url_list_query = "select url, institucion from agentdb.url_base"
    themes_query = "select tema, id_tema from agentdb.tema where id_xml is null"
    #obtener lista de temas a buscar
    themes_list = generic_query(themes_query)
    #obtener lista de urls base
    base_url_list = generic_query(base_url_list_query)
    #validar si alguna de las dos listas esta vacia
    if themes_list and base_url_list is not None:
        #iterar sobre la lista de temas
        for theme in themes_list:
            construct_url(base_url_list, theme['tema'], theme['id_tema'])
    else:
        print('listas vacias')
    
constructor_agent()