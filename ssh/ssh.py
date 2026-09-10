import paramiko as p
import threading
import requests
import os
import socket 
import sys

HOST_KEY =  p.RSAKey(filename='server.key')

SSH_PORT = 2222

class SSHServerHandler(p.ServerInterface):

    client_ip = None

    def __init__(self, client_ip, transport):
        self.client_ip = client_ip
        self.transport = transport 
        self.attempts = 0

    def check_auth_password(self, username, password ):  # this method retrieves the username, password and ip from the logger and sends it to the db_api
        self.attempts += 1 
        payload = {
            "ip": self.client_ip,
            "username": username, 
            "password": password,
        }
        try:
            requests.post(os.environ.get("INGEST_API_URL"), json=payload, timeout= 5.0)       
        except requests.RequestException as e:
            print(f'Failed to send credentials: {e}')

        if self.attempts >= 3:
            print(f"[{self.client_ip}] Max auth attempts reached. Disconnecting.")
            self.transport.close()

        return p.AUTH_FAILED

    def get_allowed_auths(self, username):   #this method sets the logging method to password
        return "publickey,password"


def handleConnection(client, addr):   # this function handles a single connection 

    transport = p.Transport(client)       #paramiko wraps the socket into ssh protocol (adding encrytption)
    transport.add_server_key(HOST_KEY)  # this uses the keys generated 

    ip = addr[0]
    server_handler = SSHServerHandler(ip, transport)

    transport.start_server(server=server_handler) # starts servers

    channel = transport.accept(1)  #wait 1 second for the channel (session, shell, exec, sftp)
    if not channel is None:    #close the channel immediately
        channel.close()




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
    threads = []
    while True:
        try: 
            client, addr = sock.accept()
            print(f"Connection from {addr[0]}:{addr[1]}")
            
            # Start a new thread for each connection without blocking
            new_thread = threading.Thread(target=handleConnection, args=(client, addr))
            new_thread.daemon = True  # Allows the program to exit even if threads are running
            new_thread.start()

        except Exception as e:
            print("*** Listen/accept failed: {}".format(e))













    