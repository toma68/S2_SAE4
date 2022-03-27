#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

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
    print(compte)
    types_articles_cout = []
    labels = []
    values = []
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
    print(compte)
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


@admin_dataviz_article.route('/admin/type-article/bilan-adresse-cp')
def show_dataviz_adresse_cp():
    mycursor = get_db().cursor()
    requete = '''select cp_adresse,count(*) from adresse group by cp_adresse;'''
    mycursor.execute(requete)
    compte= mycursor.fetchall()
    print(compte)
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
    print(compte)
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