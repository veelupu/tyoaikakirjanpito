# Copyright (c) 2021 Veera Lupunen

from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
    return render_template("index.html", items=options)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # PUUTTUU: SALASANAN JA TUNNUKSEN TARKISTAMINEN
    session["username"] = username
    return redirect("/home")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/home")
def home():
    return render_template("home.html")