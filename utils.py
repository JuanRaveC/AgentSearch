import os

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