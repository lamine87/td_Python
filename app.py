from flask import Flask, render_template, redirect, url_for, request

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

@app.route('/')
def accueil():
    produits = get_all_produits()
    # print("Produits récupérés :", produits)  # Ajout d'une instruction de débogage
    return render_template('index.html', produits=produits)


def get_all_produits():
    try:
        # Création d'un curseur pour exécuter des requêtes
        cursor = mydb.cursor()
        
        # Exécution de la requête pour récupérer tous les produits
        cursor.execute("SELECT * FROM produits")
        
        # Récupération des résultats de la requête
        produits = cursor.fetchall()
    
        # Fermeture du curseur et de la connexion à la base de données
        # cursor.close()
    
        # Retour des produits récupérés
        return produits
        
    except Exception as e:
        print(e)
        return f"Une erreur s'est produite : {str(e)}"


@app.route('/ajouter')
def page_ajouter():
    return render_template('ajouter-produit.html')


@app.route('/ajouter-produit', methods=['GET', 'POST'])
def ajouter_produit():
    if request.method == 'POST':
        # Récupérez les données du formulaire
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']

        # Insérez les données du produit dans la base de données
        cursor = mydb.cursor()
        query = "INSERT INTO produits (id, name, price) VALUES (%s, %s, %s)"
        values = (id, name, price)
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()

        return redirect('/')
    else:
        return 'Une erreur s\'est produite lors de l\'enregistrement des données'


@app.route('/edit/<int:produit_id>')
def update_produit(produit_id):
    try:
        cursor = mydb.cursor()

        # Récupérer les détails du produit en utilisant l'identifiant produit_id
        select_query = "SELECT * FROM produits WHERE id = %s"

        cursor.execute(select_query, (produit_id,))
        produits = cursor.fetchone()
        cursor.close()
 
        if produits:
            return render_template('edit.html', produits=produits)
        else:
            return redirect('/')

    except mysql.connector.Error as error:
        # print("Erreur lors de la récupération du produit :", error)
        return redirect('/')
    
@app.route('/update/<int:produit_id>', methods=['POST'])
def edit_produit(produit_id):
    try:
        cursor = mydb.cursor()
        # Récupérer les détails du produit en utilisant l'identifiant produit_id
        select_query = "UPDATE produits SET name = %s, price = %s WHERE id = %s"
        # Remplacez nom_colonne1 et nom_colonne2 par les noms réels des colonnes que vous souhaitez mettre à jour

        # Récupérez les valeurs mises à jour depuis votre formulaire HTML ou autre source
        name = request.form['name']
        price = request.form['price']

        cursor.execute(select_query, (name, price, produit_id))
        mydb.commit()
        cursor.close()
        return redirect('/')
    
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

    
@app.route('/delete/<int:produit_id>', methods=['GET'])
def delete_produit(produit_id):
    try:
        cursor = mydb.cursor()
        
        # Supprimer le produit en utilisant l'identifiant produit_id
        delete_query = "DELETE FROM produits WHERE id = %s"
        cursor.execute(delete_query, (produit_id,))
        mydb.commit()
        
        cursor.close()
        #mydb.close()

        return redirect('/')
    except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"

    

if __name__ == '__main__':
    app.run(debug = True)

