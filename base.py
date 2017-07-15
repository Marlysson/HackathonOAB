# -*- coding: utf-8 -*- 

THAMIS_FIRST_INSTANCE = 'http://www.tjpi.jus.br/themisconsulta/consulta/solr/parte'
THAMIS_SECOND_INSTANCE = 'http://www.tjpi.jus.br/e-tjpi/home/consulta/parte'

def obter_dados(nome):
	
	dados = {"nome_parte":nome}

	req = requests.post(THAMIS_FIRST_INSTANCE,parametros)

	dado = req.content

