# -*- coding: utf-8 -*- 

import PyPDF2
import requests
from bs4 import BeautifulSoup
import os

URL_DIARIO = "http://www.tjpi.jus.br/site/modules/diario/Init.mtw"

def obter_link_diario():

    conteudo = requests.get(URL_DIARIO).content
    parser = BeautifulSoup(conteudo,"html.parser")
    diario = parser.findAll("a")
    link = [elemento.get("href") for elemento in diario if elemento.get("href").endswith(".pdf")][-1]
    return link

def obter_nome_arquivo(link):
    return link.split("/")[-1]

def gravar(link):

    conteudo = requests.get(obter_link_diario()).content
    nome = obter_nome_arquivo(link)

    endereco_completo = "pdfs/"+nome

    with open(endereco_completo,"wb") as arquivo:
        arquivo.write(conteudo)

def tratar_texto(texto):
    return texto.strip().replace("\n","")

def return_text(arquivo):

    objeto_pdf = open(arquivo, 'rb')
    reader = PyPDF2.PdfFileReader(objeto_pdf)

    conteudos = []

    for num in range(reader.numPages):

        texto = tratar_texto(reader.getPage(num).extractText())
        conteudos.append(texto)

    return " ".join(conteudos)

def parsear_pdf(arquivo):
        
    DIR = "pdfs"

    arquivos = os.listdir(DIR)

    for arquivo in arquivos:

        caminho = os.path.join(DIR,arquivo)

        texto = return_text(caminho)

        nome = arquivo.split(".")[0]

        with open("parseados/"+nome+".txt","w") as file2:
            file2.write(texto)
        

parsear_pdf("pdfs/dj170714_8248.pdf")