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
        query = "SELECT * FROM players"
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

@app.route("/edit_players/<int:player_id>", methods=["POST", "GET"])
def edit_players(player_id):
    if request.method == "GET":
        query = "SELECT * FROM players WHERE player_id = %s" % (player_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_players.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Players"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form["age"]
            height = request.form["height"]
            year = request.form["year"]

        query = "UPDATE players SET players.first_name = %s, players.last_name = %s, players.age = %s, players.height = %s, players.year = %s WHERE players.player_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, age, height, year, player_id))
        mysql.connection.commit()

        return redirect("/players")
    
@app.route('/playerteams', methods=["POST", "GET"])
def playerteams():
    if request.method=="GET":
        query = "SELECT visiting_team_id, player_teams.player_id, players.first_name, players.last_name, contract_expiration FROM player_teams INNER JOIN players ON player_teams.player_id=players.player_id WHERE player_teams.player_id=players.player_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, first_name, last_name FROM players"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        query3 = "SELECT visiting_team_id, name FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visiting_team_data = cur.fetchall()

        query4 = "SELECT * FROM players WHERE players.player_id NOT IN (SELECT player_teams.player_id FROM player_teams)"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        player_team_data = cur.fetchall()

        return render_template("playerteams.j2", data=data, player_data=player_data, visiting_team_data=visiting_team_data, player_team_data=player_team_data)

    if request.method=="POST":
        if request.form.get("Add_Player_Team"):
            visiting_team_id=request.form["visiting_team_id"]
            player_id=request.form["player_id"]
            contract_expiration=request.form["contract_expiration"]

            query ="INSERT INTO player_teams (visiting_team_id, player_id, contract_expiration) VALUES (%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (visiting_team_id, player_id,contract_expiration))
            mysql.connection.commit()

            return redirect("/playerteams")


@app.route('/edit_playerteams/<int:player_id>', methods=["POST", "GET"])
def edit_playerteams(player_id):
    if request.method =="GET":
        query = "SELECT * FROM player_teams WHERE player_id = %s" %(player_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data= cur.fetchall()

        query2 = "SELECT visiting_team_id, name FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        visiting_team_data = cur.fetchall()
        
        
        return render_template("edit_playerteams.j2", data=data, visiting_team_data=visiting_team_data)

    if request.method == "POST":
        if request.form.get("Edit_PlayerTeams"):
            player_id=request.form["player_id"]
            visiting_team_id = request.form["visiting_team_id"]
            contract_expiration = request.form["contract_expiration"]


        query = "UPDATE player_teams SET player_teams.visiting_team_id = %s, player_teams.contract_expiration = %s WHERE player_teams.player_id= %s"
        cur = mysql.connection.cursor()
        cur.execute(query, ( visiting_team_id, contract_expiration, player_id))
        mysql.connection.commit()

        return redirect("/playerteams")


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
    
    app.run(port=65234, debug=True) 
