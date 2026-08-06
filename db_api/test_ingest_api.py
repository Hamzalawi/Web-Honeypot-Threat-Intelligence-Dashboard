import requests
import os
from dotenv import load_dotenv

load_dotenv()



# 1. Define your endpoint
url = os.environ.get("INGEST_API_URL")

# 2. Build your data as a normal Python dictionary
payload = {
    "username": "test_user",
    "password": "supersecretpassword",
    "ip": "8.8.8.8",
    "user_agent": "sqlmap"
}

# 3. Send the request (requests automatically sets the Content-Type header for json)
print(f"Sending POST request to {url}...")
response = requests.post(url, json=payload)

# 4. Print the results clearly
print(f"Status Code: {response.status_code}")
print("Response Body:")
print(response)