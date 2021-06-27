# Copyright (c) 2021 Veera Lupunen

from flask import Flask
from flask import redirect, render_template, request, session, jsonify
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import datetime

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
    options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, id FROM worker WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user == None:
        return render_template("index.html", items=options, message=("Oijoi, jotain meni pieleen! Tarkista, että kirjoitit tunnuksesi oikein."))
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["id"] = user[1]
            return redirect("/home")
        else:
            return render_template("index.html", items=options, message=("Oijoi! Tarkista, että kirjoitit salasanasi oikein."))    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/home", methods=["POST", "GET"])
def home():
    w_id = session["id"]
    hours = [0, 0, 0, 0]
    
    timeframe = ["day", "week", "month", "year"]
    
    for i in range(4):
        sql = """SELECT SUM (work_time) FROM (
            SELECT e.time_end-e.time_beg work_time 
            FROM entry e 
            WHERE w_id=(:w_id) 
            AND date_trunc(:timeframe, time_beg)=date_trunc(:timeframe, current_timestamp::timestamp)
            GROUP BY e.id) AS work_times"""
            
        result = db.session.execute(sql, {"w_id":w_id, "timeframe":timeframe[i]})
        work_time = result.fetchone()[0]
        
        if work_time == None:
            continue;
        
        sql = """SELECT SUM (pause) FROM (
            SELECT pause 
            FROM entry e 
            WHERE w_id=(:w_id) 
            AND date_trunc(:timeframe, time_beg)=date_trunc(:timeframe, current_timestamp::timestamp)
            GROUP BY e.id) AS work_times"""
        
        result = db.session.execute(sql, {"w_id":w_id, "timeframe":timeframe[i]})
        pause = result.fetchone()[0]
        
        db.session.commit()
        
        hours[i] = ("%.02f" % (work_time.total_seconds()/3600 - pause)).replace(".", ",")
    
    return render_template("home.html", hours=hours)
    
@app.route("/register", methods=["POST"])
def register():
    # Hae tiedot lomakkeelta
    options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
    username = request.form["username"]
    
    if len(username) > 25 or len(username) < 3:
        return render_template("index.html", items=options, message=("Liian lyhyt tai pitkä käyttäjänimi! Nimen tulee olla vähintään 3 merkkiä ja enintään 25 merkkiä pitkä."))
    
    sql = "SELECT COUNT(id) FROM worker WHERE username=(:username)"
    result = db.session.execute(sql, {"username":username})
    count = result.fetchone()[0]
    
    if count > 0:
        return render_template("index.html", items=options, message=("Voi harmi! Joku ehti jo varata tämän tunnuksen."))
    
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    
    if len(password1) < 8:
        return render_template("index.html", items=options, message=("Liian lyhyt salasana! Salasanan tulee olla vähintään 8 merkkiä pitkä."))
    
    if password1 != password2:
        return render_template("index.html", items=options, message=("Hups! Salasanat eivät täsmää. Tarkista, että kirjoitit saman salasanan molempiin kenttiin."))
    
    # Kryptaa salasana
    hash_value = generate_password_hash(password1)
    
    # Tallenna tietokantaan
    sql = "INSERT INTO worker (username, password) VALUES(:username, :password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    
    # Avaa sisäänkirjautumissivu
    return render_template("index.html", items=options, message=("Rekisteröityminen onnistui!"))

@app.route("/add-entry", methods=["GET", "POST"])
def add_entry():
    w_id = session["id"]
    
    sql = "SELECT content FROM task, worker_task w_t WHERE w_t.w_id=(:w_id) AND w_t.t_id=task.id"
    result = db.session.execute(sql, {"w_id":w_id})
    all_tasks = result.fetchall()
    all_tasks = [x[0] for x in all_tasks]
    
    db.session.commit()
    
    if request.method == "GET":
        return render_template("record.html", tasks=all_tasks)
        
    date = request.form["datepicker"]
    time_beg = request.form["time-beg"]
    time_end = request.form["time-end"]
    tasks = request.form.getlist("task")
    pause = request.form["pause"]
    notes = request.form["notes"]
    
    if pause != None:
        pause = int(pause)/60

    day = int(date[:2])
    month = int(date[3:5])
    year = int(date[6:])
    
    timeformat = "%H:%M"
    
    try:
        time_beg = datetime.datetime.strptime(time_beg, timeformat).time()
    except ValueError:
        return render_template("record.html", message="Tarkista aloituskellonaika! Anna aika muodossa hh:mm")
    
    try:
        time_end = datetime.datetime.strptime(time_end, timeformat).time()
    except ValueError:
        return render_template("record.html", message="Tarkista lopetuskellonaika! Anna aika muodossa hh:mm")
    
    time_beg = datetime.datetime.combine(datetime.date(year, month, day), time_beg)
    time_end = datetime.datetime.combine(datetime.date(year, month, day), time_end)
    
    if time_beg > time_end:
        return render_template("record.html", message="Tarkista kellonajat! Aloituskellonajan pitää olla lopetuskellonaikaa aikaisempi.")
       
    sql = "INSERT INTO entry (time_beg, time_end, pause, notes, w_id) VALUES(:time_beg, :time_end, :pause, :notes, :w_id) RETURNING id"
    result = db.session.execute(sql, {"time_beg":time_beg, "time_end":time_end, "pause":pause, "notes":notes, "w_id":w_id})
    e_id = result.fetchone()[0]
    
    sql = "INSERT INTO task_entry (t_id, e_id) SELECT id, :e_id FROM task WHERE content=ANY (:tasks)"
    db.session.execute(sql, {"e_id":e_id, "tasks":tasks})
    
    db.session.commit()
    
    return render_template("record.html", tasks=all_tasks, message="Tallennus onnistui!")

@app.route("/browse")
def browse():
    return render_template("browse.html")
    
@app.route("/browse/<timeframe>")
def browse_timeframe(timeframe):
    w_id = session["id"]
        
    sql = """SELECT e.*, e.time_end-e.time_beg work_time, array_agg(t.content) tasks
        FROM entry e 
        JOIN task_entry t_e ON e.id=t_e.e_id 
        JOIN task t ON t_e.t_id=t.id
        WHERE date_trunc(:timeframe, time_beg)=date_trunc(:timeframe, current_timestamp::timestamp)
        AND w_id=(:w_id)
        GROUP BY e.id"""
    
    result = db.session.execute(sql, {"timeframe":timeframe, "w_id":w_id})
    db.session.commit()
    
    entries = result.fetchall()
    entry_list = [{
        "id": x.id,
        "date": x.time_beg.strftime("%d.%m.%Y"),
        "time_beg": x.time_beg.strftime("%H:%M"),
        "time_end": x.time_end.strftime("%H:%M"),
        "pause": str(x.pause).replace(".", ","),
        "work_time": ("%.02f" % (x.work_time.total_seconds()/3600 - x.pause)).replace(".", ","),
        "tasks": x.tasks,
        "notes": x.notes}
        for x in entries]
    
    return jsonify(entry_list)
    
@app.route("/settings")
def manage_settings():
    # Haetaan tehtävät tietokannasta
    id = session["id"]
    
    sql = "SELECT content FROM task, worker_task w_t WHERE w_t.w_id=(:id) AND w_t.t_id=task.id"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    tasks = [x[0] for x in tasks]
    
    db.session.commit()
    
    return render_template("settings.html", id=id, tasks=tasks)
    
@app.route("/change-password", methods=["POST"])
def change_password():
    if session["username"] == "kokeilija":
        return render_template("settings.html", message="Tämän käyttäjän salasanaa ei ole mahdollista vaihtaa.")
    
    id = session["id"]
    
    sql = "SELECT password FROM worker WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    db.session.commit()
    
    hash_value = user[0]
    password_old = request.form["password-old"]
    
    if check_password_hash(hash_value,password_old):
        password_new1 = request.form["password-new1"]
        password_new2 = request.form["password-new2"]
        
        if password_new1 == password_new2:
            hash_value = generate_password_hash(password_new1)
            sql = "UPDATE worker SET password=(:hash_value) WHERE id=(:id)"
            db.session.execute(sql, {"id":id, "hash_value":hash_value})
            db.session.commit()
            return render_template("settings.html", message="Salasanan vaihtaminen onnistui!")
        else:
            return render_template("settings.html", message="Salasanan vaihtaminen epäonnistui – salasanat eivät täsmää.")
    else:
        return render_template("settings.html", message="Salasanan vaihtaminen epäonnistui – tarkista salasanasi oikeinkirjoitus.")

@app.route("/add-task", methods=["POST"])
def add_task():
    w_id = session["id"]
    content = request.form["new-task"]
    
    if len(content) > 100 or len(content) < 3:
        return render_template("settings.html", message="Liian pitkä tai lyhyt työtehtävä! Käytä vähintään 3 ja enintään 100 merkkiä.")
    
    sql = "INSERT INTO task (content) VALUES(:content) RETURNING id"
    result = db.session.execute(sql, {"content":content})
    t_id = result.fetchone()[0]
    
    sql = "INSERT INTO worker_task (w_id, t_id) VALUES(:w_id, :t_id)"
    db.session.execute(sql, {"w_id":w_id, "t_id":t_id})

    db.session.commit()
    
    return redirect("/settings")
    
    
    
    
    
    