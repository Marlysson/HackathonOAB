from flask import Flask
from flask  import jsonify
from flask import request
from flask import render_template

from finders import *
from parsers import *

app = Flask(__name__)

@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastro.html")    

@app.route('/pesquisar',methods=["POST"])
def buscar():

    dado = request.form.get("nome")
    
    finder = FinderThemisFirst()
    dados = finder.find(dado)

    if finder.is_parseable():
        
        parser = ParserThemisFirst()
        dados = parser.parse(dados)

        return jsonify(dados)

    else:

      return jsonify({})


if __name__ == '__main__':
    app.run()