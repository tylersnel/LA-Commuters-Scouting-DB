from crypt import methods
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Citations for the following functions:
# Dates 5/26/2022
# Based on:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

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
############### Players ###############################
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

@app.route("/searchplayers", methods=["POST"])
def player_search():
        if request.method == "POST":
            if request.form.get("Search_Player"):
                first_name = request.form["first_name"]
                last_name = request.form["last_name"]
                age = request.form["age"]
                height = request.form["height"]
                year = request.form["year"]
            query = "SELECT players.player_id, first_name, last_name, age, height, year, player_teams.visiting_team_id FROM players LEFT JOIN player_teams ON player_teams.player_id=players.player_id WHERE players.first_name= %s OR players.last_name= %s OR players.age= %s or players.height = %s or players.year = %s "
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, height, year))
            data = cur.fetchall()
            return render_template("searchplayers.j2", data=data)


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

############### Player Teams ###############################
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

############### Player Stats ###############################
@app.route('/player_stats', methods=["POST", "GET"])
def player_stats():
    if request.method == "GET":
        query = "SELECT player_stats.player_stats_id, players.first_name AS First, players.last_name AS Last, player_stats.points AS Points, \
        player_stats.rebounds AS Rebounds, player_stats.assists AS Assists FROM player_stats INNER JOIN players ON player_stats.player_id = players.player_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, first_name, last_name FROM players"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        return render_template("player_stats.j2", data=data, player_data=player_data)

    if request.method == "POST":
        if request.form.get("Add_Stats"):
            player_id = request.form["player_id"]
            points = request.form["points"]
            rebounds = request.form["rebounds"]
            assists = request.form["assists"]
            
        query = "INSERT INTO player_stats (player_id, points, rebounds, assists) VALUES (%s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (player_id, points, rebounds, assists))
        mysql.connection.commit()

        return redirect("/player_stats")

@app.route("/delete_player_stats/<int:player_stats_id>")
def delete_player_stats(player_stats_id):
    query = "DELETE FROM player_stats WHERE player_stats_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (player_stats_id,))
    mysql.connection.commit()

    return redirect("/player_stats")

@app.route("/edit_player_stats/<int:player_stats_id>", methods=["POST", "GET"])
def edit_player_stats(player_stats_id):
    if request.method == "GET":
        query = "SELECT player_stats.player_stats_id, players.first_name AS First, players.last_name AS Last, player_stats.points AS Points, \
        player_stats.rebounds AS Rebounds, player_stats.assists AS Assists FROM player_stats INNER JOIN players ON player_stats.player_id = players.player_id \
        WHERE player_stats_id = %s" % (player_stats_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, first_name, last_name FROM players"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        return render_template("edit_player_stats.j2", data=data, player_data=player_data)

    if request.method == "POST":
        if request.form.get("Edit_Player_Stats"):
            player_id = request.form["player_id"]
            points = request.form["points"]
            rebounds = request.form["rebounds"]
            assists = request.form["assists"]
            
        query = "UPDATE player_stats SET player_stats.player_id = %s, player_stats.points = %s, player_stats.rebounds = %s, player_stats.assists = %s WHERE player_stats.player_stats_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (player_id, points, rebounds, assists, player_stats_id))
        mysql.connection.commit()

        return redirect("/player_stats")

############### Home Game Sales ###############################
@app.route('/home_game_sales', methods=["POST", "GET"])
def home_game_sales():
    if request.method == "GET":
        query = "SELECT * FROM home_game_sales"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT visiting_team_id, name FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        visiting_team_data = cur.fetchall()

        return render_template("home_game_sales.j2", data=data, visiting_team_data=visiting_team_data)

    if request.method == "POST":
        if request.form.get("Add_Game"):
            home_game_date = request.form["home_game_date"]
            visiting_team_id = request.form["visiting_team_id"]
            tickets_sold = request.form["tickets_sold"]
            merchandise_revenue = request.form["merchandise_revenue"]
            concession_revenue = request.form["concession_revenue"]

            if visiting_team_id == "":
                query = "INSERT INTO home_game_sales (home_game_date, tickets_sold, merchandise_revenue, concession_revenue) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (home_game_date, tickets_sold, merchandise_revenue, concession_revenue))
                mysql.connection.commit()

            else:
                query = "INSERT INTO home_game_sales (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue))
                mysql.connection.commit()
    
        return redirect("/home_game_sales")



@app.route("/delete_home_game_sales/<int:home_game_id>")
def delete_home_game_sales(home_game_id):
    query = "DELETE FROM home_game_sales WHERE home_game_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (home_game_id,))
    mysql.connection.commit()

    return redirect("/home_game_sales")


@app.route("/edit_home_game_sales/<int:home_game_id>", methods=["POST", "GET"])
def edit_home_game_sales(home_game_id):
    if request.method == "GET":
            query = "SELECT * FROM home_game_sales WHERE home_game_id = %s" % (home_game_id)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            query2 = "SELECT visiting_team_id, name FROM visiting_teams"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            visiting_team_data = cur.fetchall()

            return render_template("edit_home_game_sales.j2", data=data, visiting_team_data=visiting_team_data)

    if request.method == "POST":
        if request.form.get("Edit_Home_Game_Sales"):
            home_game_date = request.form["home_game_date"]
            visiting_team_id = request.form["visiting_team_id"]
            tickets_sold = request.form["tickets_sold"]
            merchandise_revenue = request.form["merchandise_revenue"]
            concession_revenue = request.form["concession_revenue"]

        if visiting_team_id == "":
            query = "UPDATE home_game_sales SET home_game_sales.home_game_date = %s, home_game_sales.tickets_sold = %s, home_game_sales.merchandise_revenue = %s, \
            home_game_sales.concession_revenue = %s WHERE home_game_sales.home_game_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (home_game_date, tickets_sold, merchandise_revenue, concession_revenue, home_game_id))
            mysql.connection.commit()

            return redirect("/home_game_sales")

        else:
            query = "UPDATE home_game_sales SET home_game_sales.home_game_date = %s, home_game_sales.visiting_team_id = %s, home_game_sales.tickets_sold = %s, \
            home_game_sales.merchandise_revenue = %s, home_game_sales.concession_revenue = %s WHERE home_game_sales.home_game_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue, home_game_id))
            mysql.connection.commit()
    
            return redirect("/home_game_sales")

############### Visiting Teams ###############################
@app.route('/visitingteams', methods=["POST", "GET"])
def visitingteams():
    if request.method=="GET":
        query = "SELECT * FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    
        return render_template("visitingteams.j2", data=data)

    if request.method=="POST":
        if request.form.get("Add_Visiting_Team"):
            name=request.form["name"]
            city=request.form["city"]
            stadium=request.form["stadium"]
        
            query = "INSERT INTO visiting_teams (name, city, stadium) VALUES (%s,%s,%s) "
            cur = mysql.connection.cursor()
            cur.execute(query, (name, city, stadium))
            mysql.connection.commit()

            return redirect("/visitingteams")

@app.route("/delete_visiting_team/<int:visiting_team_id>")
def delete_visiting_team(visiting_team_id):
    query = "DELETE FROM visiting_teams WHERE visiting_team_id= '%s'"
    cur =mysql.connection.cursor()
    cur.execute(query, (visiting_team_id,))
    mysql.connection.commit()
    return redirect("/visitingteams")

@app.route('/edit_visiting_team/<int:visiting_team_id>', methods=["POST", "GET"])
def edit_visitingteams(visiting_team_id):
    if request.method =="GET":
        query = "SELECT * FROM visiting_teams WHERE visiting_team_id = %s" %(visiting_team_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data= cur.fetchall()
        
        return render_template("edit_visitingteams.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_VisitingTeam"):
            name = request.form["name"]
            city = request.form["city"]
            stadium = request.form["stadium"] 


        query = "UPDATE visiting_teams SET visiting_teams.name= %s, visiting_teams.city= %s, visiting_teams.stadium= %s WHERE visiting_teams.visiting_team_id= %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, city, stadium, visiting_team_id))
        mysql.connection.commit()

        return redirect("/visitingteams")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=65234, debug=True) 

 
