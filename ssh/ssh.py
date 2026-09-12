import paramiko as p
import threading
import requests
import os
import socket 
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime, timezone

# Hide the giant Paramiko stack traces when scanners or netcat drop connections
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

HOST_KEY =  p.RSAKey(filename='server.key')

SSH_PORT = 2222
MAX_CONNECTIONS = 50

class SSHServerHandler(p.ServerInterface):

    client_ip = None

    def __init__(self, client_ip, transport):
        self.client_ip = client_ip
        self.transport = transport 
        self.attempts = 0

        self.start_time = time.time()
        self.connection_timestamp = datetime.now(timezone.utc).isoformat()


    def check_auth_password(self, username, password ):  # this method retrieves the username, password and ip from the logger and sends it to the db_api

        self.attmpts += 1

        current_duration = round(time.time - self.start_time, 2 )

        # Extract threat intel fingerprints from the transport layer
        # These are populated by Paramiko after the Key Exchange (KEX) completes
        client_version = self.transport.remote_version or "Unknown"
        cipher = self.transport.remote_cipher or "Unknown"
        mac = self.transport.remote_mac or "Unknown"
        compression = self.transport.remote_compression or "Unknown"

        payload = {
            "ip": self.client_ip,
            "username": username, 
            "password": password,
            "client_version": client_version,
            "cipher": cipher,
            "mac": mac,
            "compression": compression,
            "connection_timestamp": self.conection_timestamp,
            "session_duration_seconds": current_duration
        } 
        try:
            requests.post(os.environ.get("INGEST_API_SSH_URL"), json=payload, timeout= 5.0)       
        except requests.RequestException as e:
            print(f'Failed to send credentials: {e}')

        if self.attempts >= 3:
            print(f"[{self.client_ip}] Max auth attempts reached. Disconnecting.")
            # wait 0.5 for paramiko to send AUTH_FAILED packet cleanly
            threading.Timer(0.5, self.transport.close).start()

        return p.AUTH_FAILED

    def get_allowed_auths(self, username):   #this method sets the logging method to password
        return "publickey,password"


def handleConnection(client, addr):   # this function handles a single connection 

    client.settimeout(30)

    transport = p.Transport(client)       #paramiko wraps the socket into ssh protocol (adding encrytption)
    transport.add_server_key(HOST_KEY)  # this uses the keys generated 

    ip = addr[0]
    server_handler = SSHServerHandler(ip, transport)
    try:
        transport.start_server(server=server_handler) # starts servers

        channel = transport.accept(1)  #wait 1 second for the channel (session, shell, exec, sftp)
        if not channel is None:    #close the channel immediately
            channel.close()
    except Exception as e:
        print(f'encountered an exception: {e}')



if __name__ == "__main__": 

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', SSH_PORT))
        sock.listen(100)
        print('Listening for connection ...')
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        sys.exit(1)
# wwe create 50 threads, they will wait in the background in an idle state 
    executor = ThreadPoolExecutor(max_workers=MAX_CONNECTIONS)
    while True:
        try: 
            client, addr = sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]}")

            #submits the connection to the pool
            #if all workers are busy, the connection is stored in an internal queue until a worker is available
            executor.submit(handleConnection, client, addr)

        except Exception as e:
            print("*** Listen/accept failed: {}".format(e))

