import mysql.connector
from mysql.connector import errorcode
#crear conexion generica a la db

def db_connection():
    try:
        cnx = mysql.connector.connect(user='root', password = 'admin', database='agentdb')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuario o contrasena errado")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Base de datos no existe")
        else:
            print(err)
    else:
        return cnx