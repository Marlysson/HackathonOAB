# -*- coding:utf-8 -*-

import requests
from parsers import ParserThemisFirst

class FinderThemisFirst:

	URL = 'http://www.tjpi.jus.br/themisconsulta/consulta/solr/parte'

	def find(self,nome):
		
		dados = { "consulta.nome":nome }

		request = requests.post(FinderThemisFirst.URL,dados)
		response = request.text

		return response

class FinderThemisSecond:

	URL = 'http://www.tjpi.jus.br/e-tjpi/home/consulta/parte'

	def find(self,nome):
		
		nome = nome.upper()

		dados = { "nome_parte":nome }

		request = requests.post(FinderThemisSecond.URL,dados)
		response = request.text

		return response

class FinderDiarioOficial:

	def find(self,text):
		pass

if __name__ == "__main__":

	finder = FinderThemisFirst()
	dados = finder.find("maria luiza nascimento de araújo")

	parser = ParserThemisFirst()
	dados = parser.parse(dados)
	
	print(dados)
