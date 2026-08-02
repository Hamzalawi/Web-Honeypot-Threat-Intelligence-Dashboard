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
    
    connection = get_db

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

    connection = get_db

    with connection:
        with connection.cursor() as cursor: 
            sql =   """
            select username, password from logins 
            group by username
        """
            cursor.execute(sql)
            result = cursor.fetchall() #wrong query, have to rewrite it 

    return jsonify(result)

@app.route("/stats")
def stats():
 
    pass

    #this function returns some stats such as: bots/humans pourcentage, most used tools against me 


            

