from django.core.management.base import BaseCommand, CommandError
import csv
import requests
from datetime import datetime
import nltk
nltk.download('stopwords')
from django.utils.text import slugify
from nltk.corpus import stopwords # a,de,desde,hasta,el,la,....
import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from web.utils import normalize


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
    id = datetime.now().strftime("%Y%m%d-%H%M")
    with open('./src/web/data/{}_raw.csv'.format(id), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["FECHA_SCRAP", "CATEGORIA", "FUNCION", "EMPRESA", "PUESTO", "DESCRIPCION", "URL"])
        writer.writeheader()
        for row in data_total:
            writer.writerow(row)
    return id


class Command(BaseCommand):
    help = "This is to get data from Bumeran"

    def handle(self, *args, **options):
        id = getData()
        csv_filename = "./src/web/data/{}_raw.csv".format(id)
        job_raw = pd.read_csv(csv_filename)
        job_raw['DESC_LIMPIO'] = job_raw.apply(lambda row: normalize(row['DESCRIPCION']), axis=1)
        job_vectorizer = TfidfVectorizer()
        job_matrix = job_vectorizer.fit_transform(job_raw['DESC_LIMPIO'])
        pickle.dump(job_vectorizer, open("./src/web/data/{}_job_vectorizer.pickle".format(id), "wb"))
        pickle.dump(job_matrix, open("./src/web/data/{}_job_matrix.pickle".format(id), "wb"))
        job_puesto = job_raw[['PUESTO', 'URL']]
        job_puesto.to_pickle("./src/web/data/{}_puestos.pickle".format(id))

        pickle.dump(job_vectorizer, open("./src/web/data/job_vectorizer.pickle".format(id), "wb"))
        pickle.dump(job_matrix, open("./src/web/data/job_matrix.pickle".format(id), "wb"))
        job_puesto.to_pickle("./src/web/data/puestos.pickle".format(id))