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


def getData():
    url = "https://www.bumeran.com.pe/api/avisos/searchV2?pageSize=20&page=0&sort=RELEVANTES"
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
    # FECHA_SCRAP (done), CATEGORIA (done), FUNCION (done), EMPRESA, PUESTO, DESCRIPCION
    # [{"FECHA_SCRAP": "", "CATEGORIA": "", "...."}]
    #{'number': 0, 'size': 20, 'total': 20497, 'content': [{'id': 1116336418, 'titulo': 'Analista de Créditos con Experiencia sede YURIMAGUAS', 'detalle': '¡Supérate en Caja Arequipa! Somos la Caja líder en el país y estamos en la búsqueda del mejor talento para unirse al equipo que está transformando el mundo de las microfinanzas. Te invitamos a seguir creciendo con nosotros en el puesto de Analista de Créditos con Experiencia – Ag. Yurimaguas¿Qué necesitas para postular?: Estudios universitarios inconclusos o truncos con un mínimo de tres años (6to ciclo culminado) o egresado de Instituto Superior. Experiencia laboral mínima de 01 año como analista de créditos o cargos similares en entidades financieras.(Recuerda mantener actualizada tu información tanto en la solicitud como en tu currículum, de esta manera, podremos validar tus estudios y experiencia según lo solicitado en el perfil).¿Cuáles serán tus tareas?: Promocionar el catálogo de créditos, captar clientes y evaluar sus solicitudes de crédito aplicando la normativa vigente, haciendo seguimiento hasta la recuperación de los créditos. Prospectar clientes, ofrecer y colocar los productos de créditos de Caja Arequipa.¿Qué beneficios tenemos para ti?: Incorporarte a una empresa que cuenta con la certificación de ABE (Asociación de Buenos Empleadores), estamos en el top five en el ranking Merco Talento para captar y retener talento dentro del sector financiero y estamos dentro de las 100 mejores empresas con responsabilidad social- Merco Talento, contamos con certificación ASA con calificación A-. Oportunidad de hacer línea de carrera en el sector financiero. Convenios educativos Capacitación constante Seguro de vida ley desde el primer día de trabajo. Buen clima Laboral Cobertura de Salud Programa de beneficios Siempre+Si cumples con todos los requisitos postula a la vacante, por favor adjuntar CV documentado y actualizado en formato Word o PDF.¡Muchos éxitos en este proceso de selección!De conformidad con lo señalado en la Ley N° 29733, Ley de Protección de Datos Personales y su norma reglamentaria D.S. y N° 003-2013-JUS, en el presente acto EL POSTULANTE brinda su consentimiento para que CAJA AREQUIPA, con RUC 20100209641 y domicilio en Calle La Merced N° 106, Cercado, Arequipa, pueda realizar tratamiento de sus datos personales y/o datos sensibles, sean proporcionados a través de la presente plataforma, las fichas formatos o cualquier otro documento que sea requerido por CAJA AREQUIPA, con la finalidad de recopilar los datos personales de los postulantes para gestionar el proceso de selección y evaluación a cargos laborales según el perfil solicitado, y sólo para los efectos de la misma. CAJA AREQUIPA no realiza transferencia de datos personales, salvo obligación legal y normativo.Así mismo puede ejercer sus derechos ARCO de acceso, rectificación, cancelación y oposición así como revocar su consentimiento, presentando una solicitud clara y formal en cualquiera de nuestras agencias a nivel nacional o través del correo proteccion.datos@cajaarequipa.pe.', 'aptoDiscapacitado': True, 'idEmpresa': 2222560, 'empresa': 'Caja Arequipa', 'confidencial': False, 'logoURL': 'https://imgbum.jobscdn.com/portal/img/empresas/11/static/logoMainPic_2222560_bum_vfac74043.jpg', 'fechaHoraPublicacion': '29-05-2024 23:59:20', 'fechaPublicacion': '29-05-2024', 'planPublicacion': {'id': 20, 'nombre': 'Agrupados_60Full'}, 'portal': 'bumeran', 'tipoTrabajo': 'Full-time', 'idPais': 11, 'idArea': 1, 'idSubarea': 2592, 'leido': None, 'visitadoPorPostulante': None, 'localizacion': 'Yurimaguas, Loreto', 'cantidadVacantes': 1, 'guardado': None, 'gptwUrl': None, 'match': None, 'promedioEmpresa': 4.27, 'modalidadTrabajo': 'Presencial', 'tipoAviso': 'home'}, {'id': 1116336393, 'titulo': 'Analista de Créditos con Experiencia Ag. HUANCAVELICA', 'detalle': 'Somos una institución financiera líder dentro del sistema de cajas municipales del Perú, sin fines de lucro, creada con el objetivo estratégico de constituirse en un elemento fundamental de descentralización financiera y democratización del crédito.Somos Caja Arequipa, la Caja N° 1 del Perú, y nos encontramos en búsqueda del mejor talento para formar parte del equipo que está revolucionando las Microfinanzas en nuestro país, te invitamos a postular al puesto de Analista de Créditos con Experiencia - Ag. Huancavelica¿Qué necesitas para postular?:Estudios universitarios inconclusos o truncos con un mínimo de tres años ( 6to ciclo culminado) o egresado de Instituto Superior.Experiencia laboral mínima de 0 1 año como analista de créditos o cargos similares en entidades financieras.¿Cuáles serán tus tareas?:Promocionar el catálogo de créditos, captar clientes y evaluar sus solicitudes de crédito aplicando la normativa vigente, haciendo seguimiento hasta la recuperación de los créditos.Prospectar clientes, ofrecer y colocar los productos de créditos de Caja Arequipa.¿Qué beneficios tenemos para ti?:Oportunidad de hacer línea de carrera en el sector financiero.Convenios educativosCapacitación constantePertenecer a una sólida empresa que está en crecimiento.Seguro de vida ley desde el primer día de trabajo.Buen clima LaboralSi cumples con todos los requisitos postula a la vacante, por favor adjuntar CV documentado en formato Word o PDF.¡Muchos éxitos en este proceso de selección!De conformidad con lo señalado en la Ley N° 2 9 7 3 3, Ley de Protección de Datos Personales y su norma reglamentaria D.S. y N° 0 0 3- 2 0 1 3-JUS, en el presente acto EL POSTULANTE autoriza a LA CAJA al uso de los datos personales y de los datos sensibles que pueda proporcionar en el desarrollo del proceso de postulación y solo para los efectos de la misma.', 'aptoDiscapacitado': True, 'idEmpresa': 2222560, 'empresa': 'Caja Arequipa', 'confidencial': False, 'logoURL': 'https://imgbum.jobscdn.com/portal/img/empresas/11/static/logoMainPic_2222560_bum_vfac74043.jpg', 'fechaHoraPublicacion': '29-05-2024 23:35:08', 'fechaPublicacion': '29-05-2024', 'planPublicacion': {'id': 20, 'nombre': 'Agrupados_60Full'}, 'portal': 'bumeran', 'tipoTrabajo': 'Full-time', 'idPais': 11, 'i