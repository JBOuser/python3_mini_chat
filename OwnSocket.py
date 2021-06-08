import socket

#ACTION CONSTANTS
OK = "OK"
UP = "UP"
DOWN = "DOWN"
EXIT = "EXIT"

#GLOBAL VARIABLES
server = None
client = None

def create_server(host, port):
    global server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen()
    print("Server listening at port {} (run Client.py)".format(port))    
    return server


def create_client(host, port):
    global client
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    return client


def try_close(socket):
    if(socket is not None):
        try:
            socket.close()
        except socket.error as cc:
            print("Socket close ERROR")
