import os
import csv
import magic
import pickle
import re
import nltk
nltk.download('stopwords')
from datetime import datetime
from nltk.corpus import stopwords
from django.conf import settings
from django.utils.text import slugify
from pypdf import PdfReader
import docx
import requests


job_vectorizer = pickle.load(open(os.path.join(settings.BASE_DIR, "./web/data/job_vectorizer.pickle"), "rb"))
job_matrix = pickle.load(open(os.path.join(settings.BASE_DIR, "./web/data/job_matrix.pickle"), "rb"))
ranker = pickle.load(open(os.path.join(settings.BASE_DIR, "./web/data/puestos.pickle"), "rb"))


def parseFile(filename):
    mimetype = magic.from_file(filename.name, mime=True)
    if mimetype == "application/pdf":
        reader = PdfReader(filename.name)
        number_of_pages = len(reader.pages)
        allText = ""
        for page in range(0, number_of_pages):
            page_instance = reader.pages[page]
            text = page_instance.extract_text()
            allText = allText + text
        return allText
    if mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    return None


def normalize(raw):
    # 1. Solo letras
    letras = re.sub("[^a-zA-ZáóéíúñÑ]", " ", raw)
    # 2. convertir a minusculas
    words = letras.lower().split()
    # 3. convertir a set ya que es más rapido
    stops = set(stopwords.words("spanish"))
    # 4. Quitar stop words
    meaningful_words = [w for w in words if not w in stops]
    # 5. Unir las palabras,
    result = " ".join( meaningful_words )
    # 6. reemplazar tildes
    result = result.replace("á", "a")
    result = result.replace("é", "e")
    result = result.replace("í", "i")
    result = result.replace("ó", "o")
    result = result.replace("ú", "u")
    result = result.replace("ñ", "n")
    return result


def getData(): # generate csv
    data_total = []
    for i in range(0, 10):
        url = "https://www.bumeran.com.pe/api/avisos/searchV2?pageSize=100&page={}&sort=RELEVANTES".format(i)
        data_from_bumeran = requests.post(url, headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.8,es-ES;q=0.5,es;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "x-site-id": "BMPE",
            "Origin": "https://www.bumeran.com.pe",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://www.bumeran.com.pe/empleos.html",
            "TE": "trailers",
        }, data='{"filtros":[]}')
        raw_data = data_from_bumeran.json()
        for x in raw_data["content"]:
            data_total.append({
                "FECHA_SCRAP": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "CATEGORIA": "",
                "FUNCION": "",
                "EMPRESA": x["empresa"],
                "PUESTO": x["titulo"],
                "DESCRIPCION": x["detalle"],
                "URL": "https://www.bumeran.com.pe/empleos/{}-{}-{}.html".format(slugify(x["titulo"]), slugify(x["empresa"]), x["id"]),
            })
    with open('./src/web/data/{}.csv'.format(datetime.now().strftime("%Y%m%d-%H%M")), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["FECHA_SCRAP", "CATEGORIA", "FUNCION", "EMPRESA", "PUESTO", "DESCRIPCION", "URL"])
        writer.writeheader()
        for row in data_total:
            writer.writerow(row)
    return data_total


def processData():
    filename = "./src/web/data/20240530-0219.csv"
    # migrar el jupyter a una funcion python
    # 25 minutos
