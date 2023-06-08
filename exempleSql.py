import mysql.connector
from flask import Flask
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
#  Le curseur
cursor = mydb.cursor()


# Insertion d'un produit dans la table produits
query = "INSERT INTO produits (id, name, price) VALUES (%s, %s, %s)"
values = (1, 'Samsung Galaxi', 1500) 
cursor.execute(query, values)

mydb.commit()

cursor.close()
mydb.close()
