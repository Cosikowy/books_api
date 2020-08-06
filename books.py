import os
from flask import Flask
from flask_restplus import Api, Resource, Namespace
from resources.resources import Books, DBupdate


app = Flask(__name__)

app.url_map.strict_slashes = False

''' API '''
api = Api(app, doc='/docs/', title='BOOKS API', description='Books Api')
books_api = api.namespace('books', path='/books')
db_api = api.namespace('db', path='/db')

books_api.add_resource(Books, '/<book_id>')
books_api.add_resource(Books, '/')
db_api.add_resource(DBupdate, '/')


if __name__=='__main__':
    app.run(host='localhost', port=5000, debug=True)