# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:28:57 2016

@author: Kirby Urner
"""
from flask import Flask, request, render_template
from connectors2 import Connector, elemsDB, glossaryDB, DB1, DB2
import json
import collections

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/elements/<symbol>")
def element_page(symbol):
    with Connector(elemsDB(DB1)) as dbx:
        result = dbx.seek(symbol)
    if "NOT FOUND" != result:
        if symbol != 'all':
            data = json.loads(result)
            return render_template("elem_page.html", 
                                protons=data[0],
                                elem=data[1], 
                                long_name=data[2],
                                mass=data[3],
                                series=data[4])
        else:
            data = json.loads(result)
            data = collections.OrderedDict(sorted(data.items(), 
                                            key=lambda k: k[1][0]))
            return render_template("all_elems.html", the_data=data)

    return render_template("elements.html")

@app.route("/api/elements", methods=['GET', 'POST'])
def get_elements():
    if request.method == "GET":
        elem = request.args.get('elem')
        result="NOT FOUND"
        with Connector(elemsDB(DB1)) as dbx:
            result = dbx.seek(elem) 
        if result != "NOT FOUND":
            return result
        return render_template("elements.html")
    if request.method == "POST":
        if request.form["secret"]=="DADA":
            with Connector(elemsDB(DB1)) as dbx:
                result = dbx.save(request.form)
            return result
        return "Oooo, you tried to post!"
        
@app.route("/glossary")
def glossary():
    return render_template("glossary.html")

@app.route("/glossary/<term>")
def get_glossary(term):
    with Connector(glossaryDB(DB2)) as dbx:
        result = dbx.seek(term)
    if "NOT FOUND" != result:
        if term != 'all':
            data = json.loads(result)
            return render_template("term_page.html", 
                                the_term = data[0],
                                the_definition = data[1])
        else:
            data = json.loads(result)
            data = collections.OrderedDict(sorted(data.items(), 
                                            key=lambda k: k[1][0]))
            return render_template("all_terms.html", the_data=data)

@app.route("/api/glossary", methods=['GET', 'POST'])
def get_terms():
    if request.method == "GET":
        term = request.args.get('term')
        result="NOT FOUND"
        with Connector(glossaryDB(DB2)) as dbx:
            result = dbx.seek(term) 
        if result != "NOT FOUND":
            return result
        return render_template("terms.html")
    if request.method == "POST":
        if request.form["secret"]=="DADA":
            with Connector(glossaryDB(DB2)) as dbx:
                result = dbx.save(request.form)
            return result
        return "Oooo, you tried to post!"
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)

