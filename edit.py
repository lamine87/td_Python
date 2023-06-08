from flask import Flask, render_template, request
import mysql.connector



app = Flask(__name__)
# api = Api(app)


# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    port="3301",
    user="root",
    passwd="",
    database="produit_py"  
)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_produit(id):

    if request.method == 'POST':
    
        return render_template('edit.html', produits=produits)
