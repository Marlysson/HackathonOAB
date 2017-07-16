# -*- coding:utf-8 -*-

import requests
from parsers import ParserThemisFirst
from bs4 import BeautifulSoup as bf4
import os

class FinderThemisFirst:

    URL = 'http://www.tjpi.jus.br/themisconsulta/consulta/solr/parte'

    def __init__(self):
        self.content = ""

    def find(self,nome):
        
        nome = nome.upper()

        dados = { "consulta.nome":nome }

        request = requests.post(FinderThemisFirst.URL,dados)
        response = request.text

        self.content = response

        return {"conteudo":response,"endereco":request.url}

    def is_parseable(self):

        #Verifique se o processo retornado é da mesma pessoa pesquisada
        #Se tiver mais de uma div, então mais de uma pessoa encontra,
        #Então você pesquisa não era exato.

        #TO-DO: Verifique se todo o processo retornado contém a pessoa procurada

        parser = bf4(self.content,"html.parser")
        content = parser.findAll("div",{"id":"processos"})

        if len(content):
            return False
        return True

class FinderThemisSecond:

    URL = 'http://www.tjpi.jus.br/e-tjpi/home/consulta/parte'

    def find(self,**kwargs):
        
        cpf = kwargs.get("cpf").upper()
        nome = kwargs.get("nome").upper()

        dados = { "nome_parte":nome }

        request = requests.post(FinderThemisSecond.URL,dados)
        response = request.text

        return {"conteudo":response,"endereco":request.url}

class FinderDiarioOficial:

    def find(self,**kwargs):
        pass

# if __name__ == "__main__":

#     finder = FinderThemisFirst()
#     dados = finder.find("bRUNO DARSHAN")

#     if finder.is_parseable():
        
#       parser = ParserThemisFirst()
#       dados = parser.parse(dados)

#       print(dados)

#     else:

#       print("Sua busca não foi exata.Utilize outra informação")