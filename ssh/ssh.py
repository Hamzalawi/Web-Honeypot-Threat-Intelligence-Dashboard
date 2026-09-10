import paramiko as p
import threading
import requests
import os
import socket 
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

# Hide the giant Paramiko stack traces when scanners or netcat drop connections
logging.getLogger("paramiko").setLevel(logging.ERROR)

HOST_KEY = p.RSAKey(filename='server.key')

SSH_PORT = 2222
MAX_CONNECTIONS = 50

class SSHServerHandler(p.ServerInterface):

    client_ip = None

    def __init__(self, client_ip, transport):
        self.client_ip = client_ip
        self.transport = transport 
        self.attempts = 0

    def check_auth_password(self, username, password):  # this method retrieves the username, password and ip from the logger and sends it to the db_api
        self.attempts += 1 
        payload = {
            "ip": self.client_ip,
            "username": username, 
            "password": password,
        }
        try:
            requests.post(os.environ.get("INGEST_API_URL"), json=payload, timeout=5.0)       
        except requests.RequestException as e:
            print(f'Failed to send credentials: {e}')

        if self.attempts >= 3:
            print(f"[{self.client_ip}] Max auth attempts reached. Disconnecting.")
            # Delay closure 0.5s so Paramiko flushes the AUTH_FAILED packet cleanly
            threading.Timer(0.5, self.transport.close).start()

        return p.AUTH_FAILED

    def get_allowed_auths(self, username):   # this method sets the logging method to password
        return "publickey,password"


def handleConnection(client, addr):   # this function handles a single connection 

    # Force the raw socket to drop if idle for more than 30 seconds to prevent botnet resource draining
    client.settimeout(30.0)

    transport = p.Transport(client)       # paramiko wraps the socket into ssh protocol (adding encrytption)
    transport.add_server_key(HOST_KEY)  # this uses the keys generated 

    ip = addr[0]
    server_handler = SSHServerHandler(ip, transport)

    try:
        transport.start_server(server=server_handler) # starts servers
        channel = transport.accept(30)  # wait up to 30 seconds for the channel (session, shell, exec, sftp)

        if not channel is None:    # close the channel immediately
            channel.close()
    except Exception as e:
        print(f'Encountered an exception: {e}')
    finally:
        transport.close()


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

    # --- THREAD POOL SETUP ---
    # We create exactly 50 threads up front. They will wait in the background for work.
    executor = ThreadPoolExecutor(max_workers=MAX_CONNECTIONS)
    
    while True:
        try: 
            client, addr = sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]}")

            # --- THREAD POOL MANAGEMENT ---
            # We 'submit' the connection to the pool.
            # If a worker thread is free, it starts immediately. 
            # If all 50 workers are busy, the executor automatically stores this connection 
            # in an internal queue until a worker becomes available.
            executor.submit(handleConnection, client, addr)

        except Exception as e:
            print("*** Listen/accept failed: {}".format(e)) 