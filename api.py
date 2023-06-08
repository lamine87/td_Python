import mysql.connector
from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
from werkzeug.serving import run_simple


app = Flask(__name__)
api = Api(app)


# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    port="3301",
    user="root",
    passwd="",
    database="produit_py"  
)


products = [
    {'id': 1, 'name': 'tv samsung', 'price': 1900},
    {'id': 2, 'name': 'iphone 14', 'price': 1400},
    {'id': 3, 'name': 'casque jabra 7', 'price': 300}
]

RESPONSE_OK = 200
RESPONSE_NOT_FOUND = 404
RESPONSE_CREATED = 201
RESPONSE_BAD_REQUEST = 400

class Product(Resource):
    def get(self, id):
        for product in products:
            if product['id'] == id:
                return product, RESPONSE_OK
        return 'Object not found', RESPONSE_NOT_FOUND

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        args = parser.parse_args()

        new_product = {'id': id, 'name': args['name'], 'price': args['price']}
        products.append(new_product)

        return new_product, RESPONSE_CREATED

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('price', type=float)
        args = parser.parse_args()

        for product in products:
            if product['id'] == id:
                if args['name']:
                    product['name'] = args['name']
                if args['price']:
                    product['price'] = args['price']
                return product, RESPONSE_OK

        return 'Object not found', RESPONSE_NOT_FOUND

    def delete(self, id):
        for product in products:
            if product['id'] == id:
                products.remove(product)
                return product, RESPONSE_OK
        return None, RESPONSE_NOT_FOUND

api.add_resource(Product, '/prd/<int:id>')

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app)
