from glob import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import time
from queue import Queue
from pathlib import Path
import codecs

def process_file(file_name, key_word):
    if key_word in file_name:
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(),"html.parser")
        #soup = BeautifulSoup(open(file_name), "html.parser")
        for td in soup.find_all('td'):#, {"class": "alignCenter"}):
            if td.a:
                print(td.a.text)
            else:
                print(td.text)
    else:
        pass

def process(key_word, folder_name):
    # obtener archivos a procesar
    for filename in Path(folder_name).glob('**/*.html'):
        print(filename)
        process_file(str(filename), key_word)
    else:
        print('No existen archivos a procesar')

process('java', 'HTML')

#+'/{}-*.html'.format(key_word)