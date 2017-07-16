# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup as bf4
import re
import os
from datetime import datetime

class ParserThemisFirst:

	def __init__(self):
		self.dados = {"tipo":"primeira_instancia"}
		
	def parse(self,dados):

		text = dados["conteudo"]
		self.dados["endereco"] = dados["endereco"]
		
		parser = bf4(text,"html.parser")

		processo = parser.findAll("div",{"class":"div-header"})[0].text.replace(" ","")

		data_abertura = self.obter_por_coluna(parser,"Data de Abertura")

		self.dados["data_abertura"] = self.format_data(data_abertura)

		processo = list(processo)

		for index,letra in enumerate(processo):
			if letra.isalpha():
				processo[index] = ""

		processo = "".join(processo)

		for elemento in ["(",")"," "]:
			processo = processo.replace(elemento,"")

		self.dados["processo"] = processo
		self.dados["natureza"] = self.obter_por_coluna(parser,"Natureza")
		self.dados["observacoes"] = self.obter_por_coluna(parser,"Observação(ões)")
		self.dados["status"] = self.formatar_status(self.obter_por_coluna(parser,"Status atual"))

		return self.dados

	def format_data(self,string):
		return datetime.strptime(string,'%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M:%S')

	def formatar_status(self,string):

		data, descricao = re.split(r"\s-\s",string)

		data = data.strip()
		descricao = descricao.strip()

		data = self.format_data(data)

		return " - ".join([data,descricao])

	def obter_por_coluna(self,parser,coluna):

		tabela = parser.findAll("table")[0]

		coluna_escolhida = [elemento for elemento in tabela.findAll("tr") if coluna in elemento.find("th")][0]
		valor_escolhido = coluna_escolhida.find("td").string

		return valor_escolhido


class ParserThemisSecond:

	def parse(self,text):
		pass


class ParserDiarioOficial:

	def __init__(self):
		self.dir = "pdfs"

	def parse(self,text):
		pass

class ParserJusBrasil:

	def parse(self,text):
		pass