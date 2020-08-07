import os
import json
import requests
import pprint
from datetime import datetime
from flask_restplus import reqparse
from flask_restplus import Resource


path = os.getcwd()
path_to_file = os.path.join(path, 'db_replacement.json')

class Books(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sorted', location='args')
    parser.add_argument('author', location='args')
    parser.add_argument('published_date', location='args')


    def get(self, book_id=None):
        args = self.parser.parse_args()
        
        with open(path_to_file, 'r', encoding='utf-8') as _file:
            db = json.load(_file)
        
        if book_id:
            response = self.strip_book_info(db[book_id])
            return response, 200 

        db = list(map(lambda x: self.strip_book_info(x), db.values()))
        response = []
        if args['author']:
            for book in db:
                if isinstance(args['author'], list):
                    for author in args['author']:
                        if author in book['authors']:
                            response.append(book)
                else:
                    if args['author'] in book['authors']:
                        response.append(book)
        if args['published_date']:
            for book in db:
                book_time = datetime.strptime(book['published_date'][:4], '%Y')
                filter_date = datetime.strptime(args['published_date'][:4], '%Y')
                if book_time == filter_date:
                    response.append(book)
        
        if len(response)==0:
            response = db

        if args['sorted']:
            response.sort(key=lambda book: book['published_date'])
        elif args['sorted']=='reversed':
            response.sort(key=lambda book: book['published_date'], reversed=True)

        return response, 200 

    def strip_book_info(self, book):
        book_info = {"title":book['volumeInfo']['title'],
                "authors": book['volumeInfo']['authors'],
                "published_date":book['volumeInfo']['publishedDate'], 
                }
        info = [('categories', 'categories'), ('average_rating', 'averageRating'), ('ratings_count','ratingsCount')]
        for x in info:
            try:
                book_info[x[0]] = book['volumeInfo'][x[1]]
            except KeyError:
                book_info[x[0]] = None

        try:
            book_info["thumbnail"] = book['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            book_info["thumbnail"] = None

        return book_info

    
class DBupdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q')


    def post(self, q=None):
        args = self.parser.parse_args()
        q = args['q']
        update = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={q}').json()
        try:
            with open(path_to_file, 'r', encoding='utf-8') as _file:
                db = json.load(_file)
                print('loaded')
        except Exception as e:
            print(e)
            db = {}
        
        for item in update['items']:
            for x,y in item.items():
                db[item['id']] = item

        with open(path_to_file, 'w', encoding='utf-8') as _file:
            json.dump(db,_file)
        
        return f'db updated with query: {q}', 200


