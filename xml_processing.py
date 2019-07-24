
import xml.etree.ElementTree as ET
import time
from bs4 import BeautifulSoup
from lxml import etree
from db_manager import generic_insert

SPACE = ' '
LINE = '------------------------------------------------------------------------------------------------------------' + '\n'
FOLDER_NAME = 'HTML/'
XML_INSER_QUERY = 'insert into agentdb.xml (xml) values ("{}")'

def get_date(option):
    ts = time.gmtime()
    if option == 'ts':
        date = time.strftime("%Y%m%d%H%M%S", ts)
    elif option == 'date':
        date_ = time.strftime("%c", ts)
        date_ = date_.split()
        date = date_[2] + SPACE + date_[1] + SPACE + date_[4]
    return date

def create_xml_file(data, key_word):
    tree = ET.parse('xml_base.xml')
    root = tree.getroot()
    ts = time.gmtime()
    header_date = get_date('ts')
    root.set('id', header_date)
    for child in root:
        for sub_child in child:
            if sub_child.tag == 'fecha':
                sub_child.text = get_date('date')
            elif sub_child.tag == 'consulta':
                sub_child.text = 'arroz'
            elif sub_child.tag == 'cantidad':
                sub_child.text = '100'
    counter = 1 
    #analizar cadena:
    data_list = data.split(LINE)
    for data in data_list:
        if data and '-----' not in str(data):
            resource = ET.SubElement(root, "recurso", id=str(counter))
            row_list = str(data).split('\n')
            for row in row_list:
                data_element = str(row).split(':')
                if  'Autor' in data_element[0]: 
                    str_autor = data_element[1]
                elif 'Titulo' in data_element[0]:
                    str_title = data_element[1]
                elif 'Tipo' in data_element[0]:
                    str_type = data_element[1]
                elif 'Biblioteca' in data_element[0]:
                    str_library = data_element[1]
                elif 'Descripcion' in data_element[0]:
                    str_description = data_element[1]
                    try:
                        if data_element[2]:
                            str_description += data_element[2]
                    except Exception as error:
                        print(error)
                else:
                    pass
            #adicion de tags
            resource_author = ET.SubElement(resource, "autor")
            resource_author.set('xml:space','preserve')
            author_name = ET.SubElement(resource_author, "nombres")
            author_name.set('xml:space','preserve')
            author_name.text = str_autor or "No data returned"
            author_last_name = ET.SubElement(resource_author, "apellidos")
            author_last_name.set('xml:space','preserve')
            author_last_name.text = str_autor or "No data returned"
            #tipo
            resource_type = ET.SubElement(resource, "tipo")
            resource_type.set('xml:space','preserve')
            resource_type.text = str_type or "No data returned"
            #titulo
            resource_title = ET.SubElement(resource, "titulo")
            resource_title.set('xml:space','preserve')
            resource_title.text = str_title or "No data returned"
            #catalogo
            resource_library = ET.SubElement(resource, "catalogo")
            resource_library.set('xml:space','preserve')
            if 'Carrasquilla' in str_library:
                str_library_name = 'Aleph'
                str_library_version = 'version 21'
            elif 'Teresa' in str_library:
                str_library_name = 'Janium'
                lstr_library_version = 'version 11.03'
            elif 'Humberto' in str_library:
                str_library_name = 'Educatic'
                lstr_library_version = 'version'
            else:
                str_library_name = 'Desconocido'
                lstr_library_version = 'Desconocido'
            
            library_name = ET.SubElement(resource_library, "nombre")
            library_version = ET.SubElement(resource_library, "version")
            library_name.set('xml:space','preserve')
            library_version.set('xml:space','preserve')
            library_name.text = str_library_name or "No data returned"
            library_version.text = str_library_version or "No data returned"
            #incremento del id
            counter += 1
        else:
            pass
    
    #crear archivo
    tree.write(FOLDER_NAME+key_word+"-procesado.xml", encoding='utf-8', method="xml")
    xml_string = ET.tostring(tree.getroot())
    generic_insert(XML_INSER_QUERY.format(str(xml_string).replace('"',"'" )))