import os
import magic
import pickle
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from django.conf import settings
from pypdf import PdfReader
import docx


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