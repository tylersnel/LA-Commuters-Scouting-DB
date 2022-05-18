from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


# Configuration

app = Flask(__name__)

# Routes 
#db_connection = db.connect_to_database()

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_snelgrot"
app.config["MYSQL_PASSWORD"] = "3417"
app.config["MYSQL_DB"] = "cs340_snelgrot"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/players', methods=["POST", "GET"])
def player():
    if request.method=="GET":
        query = "SELECT * FROM players;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        

        query2 = "SELECT visiting_team_id, name FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        return render_template("players.j2", data=data, team_data=team_data)
        
    if request.method =="POST":
        if request.form.get("Add_Player"):
            first_name=request.form["first_name"]
            last_name=request.form["last_name"]
            age=request.form["age"]
            height=request.form["height"]
            year=request.form["year"]

            query = "INSERT INTO players (first_name, last_name, age, height, year) VALUES  (%s, %s,%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name,age, height, year))
            mysql.connection.commit()

            return redirect("/players")

@app.route("/delete_player/<int:player_id>")
def delete_player(player_id):
    query = "DELETE FROM players WHERE player_id = '%s';"
    cur =mysql.connection.cursor()
    cur.execute(query, (player_id,))
    mysql.connection.commit()
    return redirect("/players")


@app.route('/playerstats')
def playerstats():
    return render_template("playerstats.html")

@app.route('/homegamesales')
def homegamesales():
    return render_template("homegamesales.html")

@app.route('/visitingteams')
def visitingteams():
    return render_template("visitingteams.html")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 

