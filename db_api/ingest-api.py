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