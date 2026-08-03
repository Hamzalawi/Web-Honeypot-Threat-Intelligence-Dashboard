from flask import Flask, render_template, request
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

            "ip": request.remote_addr,      #request.remote_addr gives you the IP of the machine that directly opened the TCP connection to your Flask app.
                                            # i need to change this later or i will be getting localhost as an ip address because i am running it in docker
                                            # The solution is to use Werkzeug Middleware
                                        

            "user_agent": request.headers.get("User-Agent"),
        }

        requests.post(os.environ.get("INGEST_API_URL"), json=payload)

        return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

    else:
        return render_template("admin_panel.html")
    
