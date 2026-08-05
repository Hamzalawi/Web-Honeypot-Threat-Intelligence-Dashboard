from flask import Flask, g, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db():
    if 'db' not in g:
        g.db= pymysql.connect(host=os.environ.get("DB_HOST"),
                             user=os.environ.get("DB_USER"),
                             password=os.environ.get("DB_PASSWORD"),
                             database=os.environ.get("DB_NAME"),
                            cursorclass=pymysql.cursors.DictCursor
    )
    return g.db

@app.route("/api/recent")
def recent_attacks():
    
    connection = get_db()

    with connection:
        with connection.cursor() as cursor: 
            sql =   """
            select * from logins 
            order by time desc
            limit 10
        """
            cursor.execute(sql)
            result = cursor.fetchall()

    return jsonify(result)

@app.route("/api/creds")
def most_used_creds():
    response={}
    connection = get_db()

    with connection:
        with connection.cursor() as cursor: 
            sql1 =   """
            select username, count(*) as count from logins 
            group by username
            order by count desc
            limit 5
        """
            cursor.execute(sql1)
            response["top_usernames"]= cursor.fetchall() 

            sql2 =   """
            select password, count(*) as count from logins 
            group by password
            order by count desc
            limit 5
        """
            cursor.execute(sql2)
            response["top_passwords"]= cursor.fetchall()

    return jsonify(response)

@app.route("/api/stats")
def stats():
 
    response={}
    connection = get_db()

    with connection:
        with connection.cursor() as cursor:

            sql_bot = """
                    SELECT (AVG(is_bot) * 100.0) AS bot_percentage 
                    from logins
                    """
            cursor.execute(sql_bot)
            response["bot_pourcentage"] = cursor.fetchall()

            sql_tool = """
                select user_agent, count(distinct ip) as unique_ip from logins
                where is_bot = True
                group by user_agent
                order by unique_ip desc
                limit 10
                """
            cursor.execute(sql_tool)
            response["tools"] = cursor.fetchall()

            
    return jsonify(response)

@app.route("/api/countries")
def countries():

    connection = get_db()

    with connection:
        with connection.cursor() as cursor:
            sql_countries= """
                    select country, count(*) as count from logins
                    where country != 'Unknown'
                    group by country 
                    order by count desc
                    limit 5 
            """
            cursor.execute(sql_countries)
            result = cursor.fetchall()

    return jsonify(result)

            

    #this function returns some stats such as: bots/humans pourcentage, most used tools against me (from the user_agent attribute in the case of is_bot is set to true)
# i need to correct queries 

            

