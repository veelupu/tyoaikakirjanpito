# Copyright (c) 2021 Veera Lupunen

from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
    return render_template("index.html", items=options)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
        return render_template("index.html", items=options, message=("Oijoi, jotain meni pieleen! Tarkista, että kirjoitit tunnuksesi oikein."))
    else:
        if password == user[0]:
            session["username"] = username
            return redirect("/home")
        else:
            options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
            return render_template("index.html", items=options, message=("Oijoi! Tarkista, että kirjoitit salasanasi oikein."))          
    # ***PUUTTUU**** TUNNUKSEN KRYPTAAMINEN
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/home", methods=["POST", "GET"])
def home():
    hours = [5, 34, 125, 876]
    return render_template("home.html", hours=hours)
    
@app.route("/record", methods=["GET", "POST"])
def record():
    if request.method == "GET":
        return render_template("record.html")
    elif request.method == "POST":
        # ***PUUTTUU*** tietokantaan tallentaminen
        session["running"] = True
        tasks = request.form.getlist("task")
        return render_template("record.html", tasks=tasks)
        
@app.route("/stop-recording", methods=["POST"])
def stop_recording():
    # ***PUUTTUU*** tietokantaan tallentaminen
    session["running"] = False
    return render_template("record.html")
    
@app.route("/browse")
def browse():
    return render_template("browse.html")
    