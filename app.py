# Copyright (c) 2021 Veera Lupunen

from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

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
    sql = "SELECT password, id FROM users WHERE username=:username"
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
    hours = [5, 34, 125, 876]
    return render_template("home.html", hours=hours)
    
@app.route("/register", methods=["POST"])
def register():
    # Hae tiedot lomakkeelta
    options = ["merkitä ylös työntuntisi", "pysyä kärryillä tehtyjen tuntien määrästä", "kannustaa itseäsi toisaalta töiden tekoon ja toisaalta ansaittuun lepoon."]
    username = request.form["username"]
    
    sql = "SELECT COUNT(id) FROM users WHERE username=(:username)"
    result = db.session.execute(sql, {"username":username})
    count = result.fetchone()[0]
    
    if count > 0:
        return render_template("index.html", items=options, message=("Voi harmi! Joku ehti jo varata tämän tunnuksen."))
    
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    
    if password1 != password2:
        return render_template("index.html", items=options, message=("Hups! Salasanat eivät täsmää. Tarkista, että kirjoitit saman salasanan molempiin kenttiin."))
    
    # Kryptaa salasana
    hash_value = generate_password_hash(password1)
    
    # Tallenna tietokantaan
    sql = "INSERT INTO users (username, password) VALUES(:username, :password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    
    # Avaa sisäänkirjautumissivu
    return render_template("index.html", items=options, message=("Rekisteröityminen onnistui!"))
    
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
        timebeg = result.fetchone()[0].strftime("%H.%M")
        
        # käytä id:tä liitostaulun päivittämiseen
        tasks = request.form.getlist("task")
        sql = "INSERT INTO task_entry (t_id, e_id) SELECT id, :e_id FROM task WHERE content=ANY (:tasks)"
        db.session.execute(sql, {"e_id":e_id, "tasks":tasks})
        
        db.session.commit()
        status = "käynnistetty"
        return render_template("record.html", tasks=tasks, timebeg=timebeg, id=e_id, status=status)
        
@app.route("/stop-recording", methods=["POST"])
def stop_recording():    
    # Haetaan lopetettavan tallennuksen id
    id = int(request.form["id"])
    
    # Lisätään tietokantaan tallennuksen päättymisaika
    sql = "UPDATE entry SET time_end=CURRENT_TIMESTAMP, paused=false WHERE id=(:id)"
    db.session.execute(sql, {"id":id})
    
    # Haetaan lopetettavan tallennuksen alkamisaika ja loppumisaika tietokannasta
    sql = "SELECT time_beg, time_end FROM entry WHERE id=(:id)"
    result = db.session.execute(sql, {"id":id})
    times = result.fetchall()
    
    timebeg = times[0][0].strftime("%H.%M")
    time_end = times[0][1].strftime("%H.%M")
    
    db.session.commit()
    session["running"] = False
    return render_template("record.html", timebeg=timebeg, time_end=time_end)
    
@app.route("/pause-recording", methods=["POST"])
def pause_recording():
    # Haetaan käynnissä olevan tallennuksen id
    id = int(request.form["id"])
    
    # Haetaan käynnissä olevan tallennuksen alkamisaika tietokannasta
    sql = "SELECT time_beg FROM entry WHERE id=(:id)"
    result = db.session.execute(sql, {"id":id})
    timebeg = result.fetchone()[0].strftime("%H.%M")
    
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
    
    sql = "SELECT time_beg FROM entry WHERE id=(:id)"
    result = db.session.execute(sql, {"id":id})
    timebeg = result.fetchone()[0].strftime("%H.%M")
    
    # Merkitään tiedokantaan tallennus jatkuneeksi
    sql = "UPDATE entry SET paused=false WHERE id=(:id)"
    db.session.execute(sql, {"id":id})
    
    # Haetaan käynnissä olevan tallennuksen tehtävät tietokannasta
    sql = "SELECT content FROM task, task_entry WHERE task.id=task_entry.t_id AND e_id=(:id)"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    
    db.session.commit()
    
    status = "jatkuu"
    return render_template("record.html", tasks=tasks, timebeg=timebeg, id=id, status=status)
    
@app.route("/browse")
def browse():
    return render_template("browse.html")
    
@app.route("/settings")
def manage_settings():
    # Haetaan tehtävät tietokannasta
    id = session["id"]
    
    sql = "SELECT content FROM task, users_task WHERE users_task.u_id=(:id) AND users_task.t_id=task.id"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    tasks = [x[0] for x in tasks]
    
    db.session.commit()
    
    return render_template("settings.html", id=id, tasks=tasks)
    
@app.route("/change-password", methods=["POST"])
def change_password():
    id = session["id"]
    
    sql = "SELECT password FROM users WHERE id=:id"
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
            sql = "UPDATE users SET password=(:hash_value) WHERE id=(:id)"
            db.session.execute(sql, {"id":id, "hash_value":hash_value})
            db.session.commit()
            return render_template("settings.html", message="Salasanan vaihtaminen onnistui!")
        else:
            return render_template("settings.html", message="Salasanan vaihtaminen epäonnistui – salasanat eivät täsmää.")
    else:
        return render_template("settings.html", message="Salasanan vaihtaminen epäonnistui – tarkista salasanasi oikeinkirjoitus.")


    
    
    
    
    
    
    
    