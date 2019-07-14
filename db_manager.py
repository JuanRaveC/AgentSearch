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

def generic_db_opperation(query):
    try:
        cursor.execute(query)
        return 1
    except Exception as error:
        print(error)
        print('Error realizando operacion: '+ query)
        return 0