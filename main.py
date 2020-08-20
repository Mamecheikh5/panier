from flask import Flask, request, Response, jsonify

from flask import  redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

#Pour gérer les mdp de manière hachée
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@postgresql-curly-69959/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jknjknc6v468v86v354'


db = SQLAlchemy(app)


class Commandes(db.Model):
    
    __tablename__ = 'Commande'

    id_commande= db.Column(db.Integer, primary_key=True)
    id_utilisateur=db.Column(db.Integer)
    status=db.Column(db.String(60))
    prix_in=db.Column(db.Float)
    prix_fin=db.Column(db.Float)
    id_code=db.Column(db.Integer)
    
    def __repr__(self):
        return '<Commande: {}>'.format(self.id_commande)


class l_com_stock(db.Model):
    
    __tablename__ = 'L_com_stock'
    
    id= db.Column(db.Integer, primary_key=True)
    id_commande= db.Column(db.Integer)
    id_stock= db.Column(db.Integer)
    quantite=db.Column(db.Integer)

    def __repr__(self):
        return '<L_com_stock: {}>'.format(self.id)


class stock(db.Model):
    
    __tablename__ = 'Stock'

    id_stock=db.Column(db.Integer, primary_key=True)
    id_article =db.Column(db.String(60))
    taille=db.Column(db.String(60))
    couleur=db.Column(db.String(60))
    prix_int=db.Column(db.Float)
    prix_fin=db.Column(db.Float)
    quantite =db.Column(db.Integer)
    solde=db.Column(db.Integer)
    def __repr__(self):
        return '<stock: {}>'.format(self.taille)

class article(db.Model):

    __tablename__ = 'Article'
    id_article=db.Column(db.Integer, primary_key=True)
    nom =db.Column(db.String(60))
    id_categorie=db.Column(db.Integer)
    date_publication=db.Column(db.DateTime)



    def __repr__(self):
        return '<Article: {}>'.format(self.nom)

class Code_promos(db.Model):

    __tablename__ = 'Code_promo'
    id_code=db.Column(db.Integer, primary_key=True)
    code =db.Column(db.String(60))
    pourcentage=db.Column(db.Integer)
    description=db.Column(db.String(60))


    def __repr__(self):
        return '<Code_promo: {}>'.format(self.code)


"""
    Créons une requête pour modifier le statut d'une commande 
"""    


@app.route('/addcode', methods=['POST'])
def add_code():

    commande = request.get_json()
    id_code = commande['id_code']
    code = commande['code']
    pourcentage = commande['pourcentage']
    description=commande['description']

    new_code = Code_promos(id_code=id_code,code=code,pourcentage=pourcentage,description=description)
    db.session.add(new_code)
    db.session.commit()

    return 'Succès'




@app.route('/commande/article/<int:id>', methods=['GET'])
def lister(id):
    #commande = Commandes.query.request.args.get('id')
    c = Commandes.query.get(id)
    table=[]
    articles=l_com_stock.query.filter_by(id_commande=c.id_commande).all()
    for a in articles:
        nom=article.query.filter_by(id_article=stock.query.filter_by(id_stock=a.id_stock).first().id_article).first().nom
        couleur=stock.query.filter_by(id_stock=a.id_stock).first().couleur
        idStock=stock.query.filter_by(id_stock=a.id_stock).first().id_stock
        taille=stock.query.filter_by(id_stock=a.id_stock).first().taille
        prix=stock.query.filter_by(id_stock=a.id_stock).first().prix_int
        quantite=l_com_stock.query.filter_by(id_stock=a.id_stock).first().quantite
        json_com={
        "nom": nom,
        "couleur": couleur,
        "idStock": idStock,
        "prix": prix,
        "taille": taille,
        "quantite": quantite,
        }
        table.append(json_com)
    #Renvoyons la réponse sous forme JSON
    response = jsonify({"articles":table})

    return response.json 

@app.route('/addarticle', methods=['POST'])
def add_article():
    commande = request.get_json()
    id_article = commande['id']
    nom = commande['nom']
    id_categorie = commande['id_categorie']
    date_publication=commande['date_publication']

    new_article = article(id_article=id_article,nom=nom,id_categorie=id_categorie,date_publication=date_publication)
    db.session.add(new_article)
    db.session.commit()

    return 'Succès'

@app.route('/addstock', methods=['POST'])
def add_stock():
    s = request.get_json()
    id_stock=s['id_stock']
    id_article =s['id_article']
    taille=s['taille']
    couleur=s['couleur']
    prix_int=s['prix_int']
    prix_fin=s['prix_fin']
    quantite =s['quantite']
    solde=s['solde']

    new_stock = stock(id_stock=id_stock,id_article=id_article,taille=taille,couleur=couleur,prix_int=prix_int,prix_fin=prix_fin,quantite=quantite,solde=solde)
    db.session.add(new_stock)
    db.session.commit()

    return 'Succès'

@app.route('/addcom_stock/<int:id_c>/<int:id_s>', methods=['POST'])
def add_commande_stock(id_c,id_s):
    s = request.get_json()
    id=s['id']
    id_commande= id_c
    id_stock= id_s
    quantite=s['quantite']

    new_stock = l_com_stock(id=id,id_commande=id_commande,id_stock=id_stock,quantite=quantite)
    db.session.add(new_stock)
    db.session.commit()

    return 'Succès'

@app.route('/addcommande', methods=['POST'])
def add_commande():
    s = request.get_json()
    id_commande= s['id_commande']
    id_utilisateur=s['id_utilisateur']
    status=s['status']
    prix_in=s['prix_in']
    prix_fin=s['prix_fin']
    id_code=s['id_code']

    new_commande = Commandes(id_commande=id_commande,id_utilisateur=id_utilisateur,status=status,prix_in=prix_in,prix_fin=prix_fin,id_code=id_code)
    db.session.add(new_commande)
    db.session.commit()

    return 'Succès'




@app.route('/panier/<int:id>')
def liste(id):
    
    data=[]
    code=[]
    d=[]

    
    c=None
    c=Commandes.query.filter_by(status="traitement").filter_by(id_utilisateur=id).first()
    dictionnaire={'donne':'aucune'}
    cmd=[]
    if c!=None:
        
        cmd=[Commandes.query.filter_by(status="traitement").filter_by(id_utilisateur=id).first().id_commande]
        articles=l_com_stock.query.filter_by(id_commande=c.id_commande).all()
        for a in articles:
            nom=article.query.filter_by(id_article=stock.query.filter_by(id_stock=a.id_stock).first().id_article).first().nom
            couleur=stock.query.filter_by(id_stock=a.id_stock).first().couleur
            idStock=stock.query.filter_by(id_stock=a.id_stock).first().id_stock
            taille=stock.query.filter_by(id_stock=a.id_stock).first().taille
            prix=stock.query.filter_by(id_stock=a.id_stock).first().prix_int
            quantite=l_com_stock.query.filter_by(id=a.id).first().quantite
            data.append([nom,couleur,taille,prix,quantite, idStock])

        if Commandes.query.filter_by(id_commande=c.id_commande).first() :
            code=[Code_promos.query.filter_by(id_code=Commandes.query.filter_by(id_commande=c.id_commande).first().id_code).first().code,Code_promos.query.filter_by(id_code=Commandes.query.filter_by(id_commande=c.id_commande).first().id_code).first().description,Code_promos.query.filter_by(id_code=Commandes.query.filter_by(id_commande=c.id_commande).first().id_code).first().pourcentage]

    

   
        articles=l_com_stock.query.filter_by(id_commande=c.id_commande).all()
        for a in articles:
            d.append(stock.query.filter_by(id_stock=a.id_stock).first())
        total=0
        for a , b in zip(articles,d):
            total=total+(a.quantite * b.prix_fin)


        prixCommande=[Commandes.query.filter_by(id_commande=c.id_commande).first().prix_in,Commandes.query.filter_by(id_commande=c.id_commande).first().prix_fin]
        
        Commandes.query.filter_by(id_commande=c.id_commande).update({Commandes.prix_in: total })
        Commandes.query.filter_by(id_commande=c.id_commande).update({Commandes.prix_fin: total-total/100*code[2] })

        nombre_article=len(data)
        db.session.commit()
        dictionnaire={'panier':data,'code':code,'prixCommande': prixCommande,'commande':cmd,'nombre_article':nombre_article}

    return jsonify(dictionnaire)


    
@app.route('/panier/supprimer/<int:id>/<int:id_c>',methods=['GET', 'POST'])
def supprimer(id,id_c):
    
    c=   l_com_stock.query.filter_by(id_stock=id).first().id_commande
    l_com_stock.query.filter_by(id_stock=id).filter_by(id_commande=id_c).delete()
    db.session.commit()
    return redirect(url_for(".liste",id=Commandes.query.filter_by(id_commande=c).first().id_utilisateur))

@app.route('/coupon/<int:id>',methods=['GET', 'POST'])
def changer(id):

    Commandes.query.filter_by(id_commande=id).update({Commandes.id_code: 0 })
    Commandes.query.filter_by(id_commande=id).update({Commandes.prix_fin: Commandes.prix_in })
    db.session.commit()
    return redirect(url_for(".liste",id=Commandes.query.filter_by(id_commande=id).first().id_utilisateur))


@app.route('/deleteAll',methods=['GET', 'POST'])
def delete():
    c=Commandes.query.filter_by(status='valider').all()
    for a in c:
        db.session.delete(a)
    db.session.commit()

    return 'succes'






@app.route('/appliquer/<int:id>/<string:code>',methods=['GET', 'POST'])
def appliquer(id,code):
    
    if Code_promos.query.filter_by(code=code).first() :
        Commandes.query.filter_by(id_commande=id).update({Commandes.id_code:Code_promos.query.filter_by(code=code).first().id_code })
        prix=Commandes.query.filter_by(id_commande=id).first().prix_fin
        prix=prix-(prix*Code_promos.query.filter_by(code=code).first().pourcentage/100)
        Commandes.query.filter_by(id_commande=id).update({Commandes.prix_fin: prix })
        Commandes.query.filter_by(id_commande=id).update({Commandes.id_code: Code_promos.query.filter_by(code=code).first().id_code })
        db.session.commit()
    return redirect(url_for(".liste",id=Commandes.query.filter_by(id_commande=id).first().id_utilisateur))

@app.route('/validation/<int:id>',methods=['GET', 'POST'])
def valider(id):
    
    c=Commandes(id_commande=len(Commandes.query.all())+1,id_utilisateur=Commandes.query.filter_by(id_commande=id).first().id_utilisateur,status='traitement',prix_in=0,prix_fin=0,id_code=0)
    db.session.add(c)
    Commandes.query.filter_by(id_commande=id).update({Commandes.status: 'valider' })
    db.session.commit()

    return redirect(url_for(".liste",id=Commandes.query.filter_by(id_commande=id).first().id_utilisateur))









if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')