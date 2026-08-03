from flask import Flask, g, jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db= pymysql.connect(host=os.environ.get("DB_HOST"),
                             user=os.environ.get("DB_USER"),
                             password=os.environ.get("DB_PASSWORD"),
                             database=os.environ.get("DB_NAME"),
                            cursorclass=pymysql.cursors.DictCursor
    )
    return g.db

@app.route("/")
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

@app.route("/creds")
def most_used_creds():
    response={}
    connection = get_db()

    with connection:
        with connection.cursor() as cursor: 
            sql1 =   """
            select username from logins 
            group by username
            order by count(*) desc
            limit 5
        """
            cursor.execute(sql1)
            response["top_usernames"]= cursor.fetchall() #wrong query, have to rewrite it 

            sql2 =   """
            select password from logins 
            group by password
            order by count(*) desc
            limit 5
        """
            cursor.execute(sql2)
            response["top_passwords"]= cursor.fetchall()

    return jsonify(response)

@app.route("/stats")
def stats():
 
    response={}
    connection = get_db()

    with connection:
        with connection.cursor() as cursor:

            sql_bot = """
                    select ip from logins 
                    group by is_bot
                    """
            cursor.execute(sql_bot)
            response["bot_pourcentage"] = cursor.fetchall()

            sql_tool = """
                select user_agent, count(distinct ip) from logins
                where is_bot = True
                group by user_agent
                limit 10
                """
            cursor.execute(sql_tool)
            response["tools"]
    return jsonify(response)


            

    #this function returns some stats such as: bots/humans pourcentage, most used tools against me 


            

