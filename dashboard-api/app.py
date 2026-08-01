from flask import Flask
import pymysql
import os
from dotenv import load_dotenv


app = Flask(__name__)


connection = pymysql.connect(host=os.environ.get("DB_HOST"),
                             user=os.environ.get("DB_USER"),
                             password=os.environ.get("DB_PASSWORD"),
                             database=os.environ.get("DB_NAME"),
                            cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def recent_attacks():

    with connection:
        with connection.cursor() as cursor: 
            sql =   """
            select * from logins 
            order by time desc
            limit 10
        """
            cursor.execute(sql)
            result = cursor.fetchone()

    return result

def most_used_creds():
    pass 


def stats():
    pass 

    #this function returns some stats such as: bots/humans pourcentage, most used tools against me 


            

