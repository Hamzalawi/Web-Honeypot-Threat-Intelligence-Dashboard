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

            "ip": request.remote_addr,      #request.remote_addr gives you the IP of the machine that directly opened the TCP connection to your Flask app.
                                            # i need to change this later or i will be getting localhost as an ip address because i am running it in docker
                                            # The solution is to use Werkzeug Middleware
                                        

            "user_agent": request.headers.get("User-Agent"),
        }
        print(payload)

        try:  #this will be changed later, it this specific for debugging: in the case of an error i should just return service unavailable for now

            response = requests.post(os.environ.get("INGEST_API_URL"), json=payload, timeout=5.0)

            response.raise_for_status()

            return render_template("admin_panel.html", error="Invalid username or password. Please try again.")

        except requests.exceptions.Timeout:
        # Triggered if the server takes longer than 5.0 seconds to send data
            app.logger.error("Ingest API timed out.")
            return jsonify({"error": "The Ingest API took too long to respond."}), 504

        except requests.exceptions.ConnectionError:
            # Triggered if the API is down, DNS fails, or network is disconnected
            app.logger.error("Failed to connect to Ingest API.")
            return jsonify({"error": "Could not connect to the Ingest API. It may be offline."}), 502

        except requests.exceptions.HTTPError as err:
            # Triggered by raise_for_status() for 4xx and 5xx errors
            status_code = response.status_code
            app.logger.error(f"Ingest API returned HTTP error {status_code}: {err}")
            return jsonify({
                "error": "Ingest API rejected the request.",
                "upstream_status": status_code,
                "details": response.text # Optional: captures the error message from the API
            }), status_code

        except requests.exceptions.RequestException as err:
            # Catch-all for any other requests-related issues (e.g., Invalid URL, Missing Schema)
            app.logger.error(f"An unexpected request error occurred: {err}")
            return jsonify({"error": "An internal server error occurred while contacting the Ingest API."}), 500

    else:
        return render_template("admin_panel.html")
    
