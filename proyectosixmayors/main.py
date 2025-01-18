from bs4 import BeautifulSoup
import requests
import pandas as pd

def extraer_datos_wikipedia(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }#esto es siempre igual, lo habilita para levantar como si fuera un navegador.

    #request tipo get donde le paso la url y la cabecera para que se comporte como un agente
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    
    #pasar la información que nos ha venido en el response a html
    parseo_to_html = BeautifulSoup(response.content, "html.parser") #aquí deberíamos tener todo el contenido del html.

    #coger la información que queremos scrapear:
    # Manejar contenido principal de forma segura
    contenido_principal = parseo_to_html.find("div", id="mw-content-text") #el id siempre existe en Wikipedia.
    contenido_texto = contenido_principal.getText() if contenido_principal else "Contenido principal no encontrado."

    #hacemos el dataframe
    datos = {
        "titulo": parseo_to_html.find("title").getText() if parseo_to_html.find("title") else "Título no encontrado.",
        "enlaces": [a.getText() for a in parseo_to_html.findAll("a")[:10] if a.getText()],
        "imagenes": [img.get("src") for img in parseo_to_html.findAll("img")[:5] if img.get("src")],
        "principal_content": contenido_texto
    }
    return datos


lista = ["https://es.wikipedia.org/wiki/Maratón_de_Berlín","https://es.wikipedia.org/wiki/Maratón_de_Nueva_York", "https://es.wikipedia.org/wiki/Maratón_de_Chicago","https://es.wikipedia.org/wiki/Maratón_de_Boston", "https://es.wikipedia.org/wiki/Maratón_de_Tokio","https://es.wikipedia.org/wiki/Maratón_de_Londres"]

for url in lista:
    datos_maratones = extraer_datos_wikipedia(url)
    if datos_maratones:
          print("Título de la página:", datos_maratones["titulo"])
          print("Primeros 10 enlaces:", datos_maratones["enlaces"])
          print("Primeras 5 imágenes:", datos_maratones["imagenes"])
          print("Contenido principal:", datos_maratones["principal_content"])

