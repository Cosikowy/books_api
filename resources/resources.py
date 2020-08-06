import json
import requests
import pprint
from flask_restplus import reqparse
from flask_restplus import Resource




class Books(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sorted', location='args')
    parser.add_argument('author', location='args')
    parser.add_argument('publishedDate', location='args')
    # parser.add_argument('sorted', location='args')


    def get(self, book_id=None):
        args = self.parser.parse_args()
        print(args)
        
        # try:
        with open('./db_replacement.json', 'r', encoding='utf-8') as _file:
            db = json.load(_file)
        # except:
        #     db = {}
        #     return 'DB is empty update required'
        response = {}

        # pprint.pprint(db['items'][9])



        return ('', args), 200, 

    def prepare_response(self, books, **kwargs):
        pass

    
class DBupdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q')


    def post(self, q=None):
        args = self.parser.parse_args()
        q = args['q']
        update = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={q}').json()
        try:
            with open('./db_replacement.json', 'r') as _file:
                db = json.load(_file)
        except:
            db = {}
        
        if not db:
            db = {} 
        
        db.update(update)

        with open('./db_replacement.json', 'w', encoding='utf-8') as _file:
            json.dump(db,_file)
        
        return f'db updated with query: {q}', 200


