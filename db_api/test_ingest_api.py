import requests
import os
from dotenv import load_dotenv

load_dotenv()


def node1():
# 1. Define your endpoint
    url = os.environ.get("INGEST_API_URL")

    # 2. Build your data as a normal Python dictionary
    payload = {
        "username": "ahmed",
        "password": "",
        "ip": "8.8.8.8",
        "user_agent": "mozzila"
    }

    # 3. Send the request (requests automatically sets the Content-Type header for json)
    print(f"Sending POST request to {url}...")
    response = requests.post(url, json=payload)

    # 4. Print the results clearly
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response)

def node2():
    url = "http://127.0.0.1:4000/ssh"

    payload = {
        "ip": "8.8.8.8",
        "username": "",
        "password": "ali",
        "mac": "hmac-sha2-256",
        "compression": None, 
        "cipher": "EDH", 
        "client_version": "local"
    }

    print(f"Sending POST request to {url}...")
    response = requests.post(url, json=payload)

    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response)

node2()