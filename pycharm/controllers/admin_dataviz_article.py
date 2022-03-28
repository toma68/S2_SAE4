#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import random
from connexion_db import get_db

admin_dataviz_article = Blueprint('admin_dataviz_article', __name__,
                        template_folder='templates')

@admin_dataviz_article.route('/admin/type-article/bilans')
def bilans():
    return(render_template('admin/dataviz/panel-etat.html'))

@admin_dataviz_article.route('/admin/type-article/bilan-stock')
def show_type_article_stock():
    mycursor = get_db().cursor()
    requete = '''SELECT SUM(stock) as somme, libelle_vetement FROM est_dispo join vetement on est_dispo.id_vetement = vetement.id_vetement GROUP BY est_dispo.id_vetement'''
    mycursor.execute(requete)
    compte= mycursor.fetchall()
    types_articles_cout = []
    labels = []
    values = []
    for key in compte:
        labels.append(key['libelle_vetement'])
        values.append(key['somme'])
    cout_total = 0
    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values, compte=compte)


@admin_dataviz_article.route('/admin/type-article/bilan-wishlist')
def show_dataviz_wishlist():
    mycursor = get_db().cursor()
    requete = '''SELECT libelle_vetement, COUNT(*) from envie
    join vetement on vetement.id_vetement = envie.id_vetement
     group by envie.id_vetement;'''
    mycursor.execute(requete)
    compte= mycursor.fetchall()
    labels = []
    values = []
    for key in compte:
        labels.append(key['libelle_vetement'])
        values.append(key['COUNT(*)'])
    types_articles_cout = []
    cout_total = 0

    requete = '''SELECT vetement.id_vetement,libelle_vetement,COUNT(consulte.id_vetement) as nb
    from consulte 
    right join vetement on vetement.id_vetement= consulte.id_vetement
    group by vetement.id_vetement
    order by nb DESC'''
    mycursor.execute(requete)
    history = mycursor.fetchall()

    mycursor = get_db().cursor()
    requete = '''select id_vetement, DATE(date_historique) as date_historique ,count(*) from consulte 
    group by DATE(date_historique),id_vetement 
    order by date_historique;'''
    mycursor.execute(requete)
    histodate = mycursor.fetchall()

    mycursor = get_db().cursor()
    requete = '''select distinct id_vetement from consulte;'''
    mycursor.execute(requete)
    lesids = mycursor.fetchall()

    mycursor = get_db().cursor()
    requete = '''select distinct DATE(date_historique) as date_historique from consulte order by date_historique ;'''
    mycursor.execute(requete)
    lesdates = mycursor.fetchall()

    labels2 = []
    values2 = []
    i=0
    for key in lesids:
        values2.append({'id':key['id_vetement']})
        values2[i]["val"] =[]
        values2[i]["col"]=(str(random.randint(1, 255))+","+str(random.randint(1, 255))+","+str(random.randint(1, 255)))
        i+=1

    for key in lesdates:
        labels2.append(key['date_historique'])
        i=0
        for key2 in lesids:
            requete = '''SELECT count(*) from consulte where id_vetement = %s and DATE(date_historique)=%s group by DATE(date_historique);'''
            mycursor.execute(requete, (key2['id_vetement'],key['date_historique']))
            temp = mycursor.fetchone()
            if (temp == None):
                values2[i]["val"].append(0)
            else:
                values2[i]["val"].append(temp['count(*)'])
            i+=1









    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values, compte=compte, history=history,nameEtat="Wishlist",labels2=labels2,values2=values2)

@admin_dataviz_article.route('/admin/type-article/bilan-vetement/<int:id>')
def show_dataviz_article(id):
    mycursor = get_db().cursor()
    requete = '''select * from vetement where id_vetement = %s'''
    mycursor.execute(requete,(id))
    article = mycursor.fetchone()
    requete = '''SELECT vetement.id_vetement, COUNT(*) as nombre from envie
    join vetement on vetement.id_vetement = envie.id_vetement
    where envie.id_vetement = %s
    group by envie.id_vetement;'''
    mycursor.execute(requete,(id))
    compte = mycursor.fetchone()
    if (compte == None or compte['nombre'] == None):
        compte = {}
        compte['nombre'] = 0
    print(compte)

    requete = '''SELECT vetement.id_vetement,libelle_vetement,COUNT(consulte.id_vetement) as nb
    from consulte 
    right join vetement on vetement.id_vetement= consulte.id_vetement
    WHERE vetement.id_vetement=%s
    group by vetement.id_vetement
    order by nb DESC'''
    mycursor.execute(requete,(id))
    history = mycursor.fetchone()
    if (history['nb'] == None):
        history = {}
        history['nb'] = 0
    print(history)

    requete = '''SELECT count(id_commande) as cnt, sum(quantite) as sum from ligne_commande where id_vetement = %s GROUP by id_vetement'''
    mycursor.execute(requete,(id))
    commande = mycursor.fetchone()
    if (commande == None):
        commande = {}
        commande['cnt'] = 0
        commande['sum'] = 0



    mycursor = get_db().cursor()
    requete = '''select DATE(date_historique) as date_historique ,count(*) from consulte where id_vetement = %s group by DATE(date_historique);'''
    mycursor.execute(requete,(id))
    histodate = mycursor.fetchall()
    print(histodate)
    labels = []
    values = []
    for key in histodate:
        labels.append(key['date_historique'])
        values.append(key['count(*)'])
    types_articles_cout = []






    return render_template('admin/dataviz/etat_article.html',compte=compte,history=history,article=article, commande=commande, values=values,labels=labels)


@admin_dataviz_article.route('/admin/type-article/bilan-adresse-cp')
def show_dataviz_adresse_cp():
    mycursor = get_db().cursor()
    requete = '''select cp_adresse,count(*) from adresse group by cp_adresse;'''
    mycursor.execute(requete)
    compte= mycursor.fetchall()
    labels = []
    values = []
    for key in compte:
        labels.append(key['cp_adresse'])
        values.append(key['count(*)'])
    types_articles_cout = []

    cout_total = 0
    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values, compte=compte)


@admin_dataviz_article.route('/admin/type-article/bilan-com')
def show_dataviz_com():
    mycursor = get_db().cursor()
    requete = '''SELECT libelle_vetement, COUNT(*) from commentaires
     join vetement on vetement.id_vetement = commentaires.id_vetement
     group by commentaires.id_vetement;'''
    mycursor.execute(requete)
    compte= mycursor.fetchall()
    labels = []
    values = []
    for key in compte:
        labels.append(key['libelle_vetement'])
        values.append(key['COUNT(*)'])
    types_articles_cout = []

    cout_total = 0
    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values, compte=compte)

