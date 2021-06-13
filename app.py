# Copyright (c) 2021 Veera Lupunen

from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
import sys

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
    
@app.route("/start-recording", methods=["GET", "POST"])
def start_recording():
    if request.method == "GET":
        return render_template("record.html")
    elif request.method == "POST":
        session["running"] = True
        
        # luo entry-tauluun tämä tallennus käyttämällä sql-aikaleimaa ja muistiinpanoja
        # ***PUUTTUU*** muistiinpanojenkirjoitusmahdollisuus
        notes = request.form["notes"]
        sql = "INSERT INTO entry (time_beg, paused, notes) VALUES(CURRENT_TIMESTAMP, false, :notes) RETURNING id"
        
        # palauta juuri luodun tallennuksen id
        result = db.session.execute(sql, {"notes":notes})
        e_id = result.fetchone()[0]
        
        #haetaan aloitusaika, jotta se voidaan näyttää sivulla
        sql = "SELECT time_beg FROM entry WHERE id=(:id)"
        result = db.session.execute(sql, {"id":e_id})
        timebeg = result.fetchone()[0]
        
        # käytä id:tä liitostaulun päivittämiseen
        tasks = request.form.getlist("task")
        sql = "INSERT INTO task_entry (t_id, e_id) SELECT id, :e_id FROM task WHERE content=ANY (:tasks)"
        db.session.execute(sql, {"e_id":e_id, "tasks":tasks})
        
        db.session.commit()
        status = "käynnistetty"
        return render_template("record.html", tasks=tasks, timebeg=timebeg, id=e_id, status=status)
        
@app.route("/stop-recording", methods=["POST"])
def stop_recording():    
    sys.stderr.write("mitähän tapahtuu 1\n")
    # Haetaan lopetettavan tallennuksen id
    id = int(request.form["id"])
    
    sys.stderr.write("mitähän tapahtuu 2\n")
    # Lisätään tietokantaan tallennuksen päättymisaika
    sql = "UPDATE entry SET time_end=CURRENT_TIMESTAMP, paused=false WHERE id=(:id)"
    db.session.execute(sql, {"id":id})
    
    sys.stderr.write("mitähän tapahtuu 3\n")
    # Haetaan lopetettavan tallennuksen alkamisaika ja loppumisaika tietokannasta
    sql = "SELECT time_beg, time_end FROM entry WHERE id=(:id)"
    result = db.session.execute(sql, {"id":id})
    times = result.fetchall()
    
    timebeg = times[0][0]
    time_end = times[0][1]
    
    db.session.commit()
    sys.stderr.write("mitähän tapahtuu 4\n")
    session["running"] = False
    return render_template("record.html", timebeg=timebeg, time_end=time_end)
    
@app.route("/pause-recording", methods=["POST"])
def pause_recording():
    # Haetaan käynnissä olevan tallennuksen id
    id = int(request.form["id"])
    
    # Haetaan käynnissä olevan tallennuksen alkamisaika tietokannasta
    sql = "SELECT time_beg FROM entry WHERE id=(:id)"
    result = db.session.execute(sql, {"id":id})
    timebeg = result.fetchone()[0]
    
    # Haetaan käynnissä olevan tallennuksen tehtävät tietokannasta
    sql = "SELECT content FROM task, task_entry WHERE task.id=task_entry.t_id AND e_id=(:id)"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    
    sql = "UPDATE entry SET paused=true WHERE id=(:id)"
    db.session.execute(sql, {"id":id})
    
    db.session.commit()
    status = "keskeytetty"
    return render_template("record.html", tasks=tasks, timebeg=timebeg, id=id, status=status)
    
@app.route("/continue-recording", methods=["POST"])
def continue_recording():
    # Haetaan käynnissä olevan tallennuksen id
    id = int(request.form["id"])
    
    # Merkitään tiedokantaan tallennus jatkuneeksi
    sql = "UPDATE entry SET paused=false WHERE id=(:id)"
    db.session.execute(sql, {"id":id})
    
    # Haetaan käynnissä olevan tallennuksen tehtävät tietokannasta
    sql = "SELECT content FROM task, task_entry WHERE task.id=task_entry.t_id AND e_id=(:id)"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    
    db.session.commit()
    
    status = "jatkuu"
    return render_template("record.html", tasks=tasks, id=id, status=status)
    
@app.route("/browse")
def browse():
    return render_template("browse.html")
    