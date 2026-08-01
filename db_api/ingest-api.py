from flask import Flask, request
import pymysql
from dotenv import load_dotenv
import os

 
load_dotenv()



app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def insert_log():

    data = request.get_json()

    connection = pymysql.connect(host=os.environ.get("DB_HOST"),
                             user=os.environ.get("DB_USER"),
                             password=os.environ.get("DB_PASSWORD"),
                             database=os.environ.get("DB_NAME")
    )


    # I need to add these things: 
    #        - findinng the country corresponding to each IP 
    #        - finding if the attacker is a bot or a human
    # Well for the latter point, i may later need to change the logic if i want to make it more complexe (using rate of requests and request pattern) but for now keep it simple                        
    
    with connection:
        with connection.cursor() as cursor: 

            sql = "insert into logins (ip, user_agent, username, password ) values (%s, %s, %s, %s )" 

            values= (
                data.get('address'),
                data.get('user_agent'),
                data.get("username"),
                data.get("password")
            )

            cursor.execute(sql, values)
        connection.commit()
    return {"status": "success"}, 201