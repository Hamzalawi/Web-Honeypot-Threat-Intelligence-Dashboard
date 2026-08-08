from flask import Flask, g, request
import pymysql
from dotenv import load_dotenv
import os
import requests
from dbutils.pooled_db import PooledDB

load_dotenv()



app = Flask(__name__)

pool = PooledDB(
        creator=pymysql,
        mincached=5,
        maxcached=15,
        maxconnections=20,
        blocking=True,
        ping=1,
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
)


def get_db():
    if 'db' not in g:
        g.db = pool.connection()

    return g.db



BOTS=set()

with open("bad_agents.txt", "r") as f:
        BOTS={line.strip().lower() for line in f}



def geo_ip_lookup(ip):

    if ip in ('localhost', '127.0.0.1'):
        return "testing, debugging"
    else:

        try:
            response = requests.get(f"https://json.geoiplookup.io/{ip}", timeout=3) #response is a Responsone object; i.e raw string of text foromatted as json
            data = response.json() 
        except Exception:
            data = {'country_name':'not available'}

                    # .json() parses the string into a Python Dictionary
        country = data.get('country_name', 'unkown')

        return country

def verify_bot(user_agent):


    if user_agent == None :
        return False

    if user_agent.lower() in BOTS:
        return True

    else:
        return False
# obv this logic is vulnerable to UA spoofing
#also i don't think this is what i really want; curl is considered a bot, but i am searching to knonw if there is a human in the loop or not 

@app.teardown_appcontext
def close_db(error):

    if 'db' in g:
        g.db.close()

@app.route("/logs", methods=["POST"])
def insert_log():

    data = request.get_json()

    ip =  data.get('ip')
    user_agent = data.get('user_agent')
    username = data.get("username")
    password = data.get("password")
    country = geo_ip_lookup(ip)
    is_bot = verify_bot(user_agent)

    
    connection = get_db()
    with connection.cursor() as cursor: 

        sql = "insert into logins (ip, user_agent, is_bot, username, password, country ) values (%s, %s, %s, %s, %s, %s)" 

        values= (
                ip,
                user_agent,
                is_bot,
                username,
                password, 
                country
        )

        cursor.execute(sql, values)
    connection.commit()
        
    return {"status": "success"}, 201