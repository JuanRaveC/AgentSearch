import os
from db_connection import db_connection

#crear carpeta para guardar datos obtenidos
def create_data_dir(directory):
    if not os.path.exists(directory):
        print('Creando carpeta ' + directory)
        os.makedirs(directory)

# Crea archivo en carpeta especificada
def create_data_files(folder_name, file_name, data):
    file_to_create = os.path.join(folder_name, file_name+'.html')
    if not os.path.isfile(file_to_create):
        write_file(file_to_create, data)

#funcion generica para escribir en archivo
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def retreive_information(key_word):
    query = "select * from agentdb.historial where palabra_clave like '%{}%' limit 1".format(key_word)
    xml_query = "select * from agentdb.xml where id_xml = {}".format(key_word)
    print(query)
    conn = db_connection()
    # crea cursor de tipo dict
    cursor = conn.cursor()
    result_set = ''
    try:
        cursor.execute(query)
        result_set = cursor.fetchone()
        if result_set[3] is not None:
            cursor.execute(xml_query)
            xml_file = cursor.fetchone()
            return str(xml_file)
    except Exception as error:
        print(error)
        print('No se pudo obtener historial')
        return ''