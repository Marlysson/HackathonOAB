
import PyPDF2
import requests
from bs4 import BeautifulSoup
import os


class CapturarLink:

    URL_DIARIO = "http://www.tjpi.jus.br/site/modules/diario/Init.mtw"

    def __init__(self,next_pipe=None):
        self.next_pipe = next_pipe

    def run(self):

        conteudo = requests.get(CapturarLink.URL_DIARIO).content
        parser = BeautifulSoup(conteudo,"html.parser")
        diario = parser.findAll("a")
        link = [elemento.get("href") for elemento in diario if elemento.get("href").endswith(".pdf")][-1]

        instancia = object.__new__(SalvarDiario)
        instancia.__init__(link)

        self.next_pipe = instancia
        self.next_pipe.run()

class SalvarDiario:

    def __init__(self,link_diario,next_pipe=None):
        self.link_diario = link_diario
        self.next_pipe = next_pipe
        
    def obter_nome_arquivo(self,link):
        return link.split("/")[-1]

    def run(self):

        conteudo = requests.get(self.link_diario).content

        nome = self.obter_nome_arquivo(self.link_diario)

        completo = "pdfs/"+nome

        with open(completo,"wb") as arquivo:
            arquivo.write(conteudo)


        instancia = object.__new__(ConverterEmTexto)        
        instancia.__init__(nome)

        self.next_pipe = instancia
        self.next_pipe.run()

class ConverterEmTexto:

    def __init__(self,arquivo_disco,next_pipe=None):
        self.caminho_arquivo = os.path.join("pdfs",arquivo_disco)
        self.next_pipe = next_pipe

    def tratar_texto(self,texto):
        return texto.strip().replace("\n","")

    def run(self):

        objeto_pdf = open(self.caminho_arquivo, 'rb')
        reader = PyPDF2.PdfFileReader(objeto_pdf)

        conteudos = []

        for num in range(reader.numPages):

            texto = reader.getPage(num).extractText()
            conteudos.append(texto.encode("utf-8"))

        instancia = object.__new__(GravarConvertido)
        instancia.__init__(self.caminho_arquivo," ".join(conteudos))

        self.next_pipe = instancia
        self.next_pipe.run()
            
class GravarConvertido:

    def __init__(self, arquivo_disco, texto, next_pipe=None):
        self.arquivo_disco = arquivo_disco
        self.texto = texto
        self.dir_parseados = "parseados/"

    def run(self):
        
        nome,extensao = os.path.splitext(os.path.basename(self.arquivo_disco))
        nome = nome + ".txt"

        diretorio = os.path.join(self.dir_parseados,nome)

        with open(diretorio,"w") as file:
            file.write(self.texto)


class Pipeline:
    def __init__(self):
        self.pipes = []

    def pipe(self,pipe):
    
        if len(self.pipes) :
            
            atual = self.pipes[-1]
            atual.next_pipe = pipe

        self.pipes.append(pipe)

    def run(self):

        instancia = object.__new__(type(self.pipes[0]()))
        instancia.run()

if __name__ == '__main__':

    pipeline = Pipeline()

    pipeline.pipe(CapturarLink)
    pipeline.pipe(SalvarDiario)
    pipeline.pipe(ConverterEmTexto)
    pipeline.pipe(GravarConvertido)

    pipeline.run()