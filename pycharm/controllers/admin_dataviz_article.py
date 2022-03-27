#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_dataviz_article = Blueprint('admin_dataviz_article', __name__,
                        template_folder='templates')

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


@admin_dataviz_article.route('/admin/article/bilan')
def show_article_bilan():
    mycursor = get_db().cursor()

    types_articles_cout = []
    labels = []
    values = []
    cout_total = 0
    return render_template('admin/dataviz/etat_article_vente.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values)
