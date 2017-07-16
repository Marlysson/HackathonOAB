import tornado.ioloop
import tornado.web
from finders import FinderThemisFirst
from parsers import ParserThemisFirst
import json

class ThemisFirst(tornado.web.RequestHandler):
    def get(self):

        finder = FinderThemisFirst()
        dados = finder.find("Bruno Darshan")

        if finder.is_parseable():

          parser = ParserThemisFirst()
          dados = parser.parse(dados)
          print(dados)
          return dados

        else:
            
            return {}

def make_app():
    return tornado.web.Application([
        (r"/", ThemisFirst),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()