import socket
from threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None
CLIENTS = {}

def setup():
    print('\n')
    print('\t\t\t\t\t\tLudo')

    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)

    print('\t\t\t\tServer is Waiting for incoming Connection\n')
    accept_connections()

def accept_connections():
    global SERVER
    global CLIENTS
    while True:
        player_socket,addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        if (len(CLIENTS.keys())==0):
            CLIENTS[player_name] = {'player_type':'player1'}
        else:
            CLIENTS[player_name] = {'player_type':'player2'}
        
        CLIENTS[player_name]['player_socket'] = player_socket
        CLIENTS[player_name]['address'] = addr
        CLIENTS[player_name]['player_name'] = player_name
        CLIENTS[player_name]['turn'] = False
        print(F'Connection Established with {player_name}:{addr}')
        thread = Thread(target = handle_client,args = (player_socket,player_name))
        thread.start()

def handle_client(player_socket,player_name):
    global CLIENTS

    player_type = CLIENTS[player_name]['player_type']
    if player_type == 'player1':
        CLIENTS[player_name]['turn'] = True
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())
    
    else:
        CLIENTS[player_name]['turn'] = False
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())

    while True:
        try:
            message = player_socket.recv(2048)
            if message:
                for c_name in CLIENTS:
                    c_socket = CLIENTS[c_name]['player_socket']
                    c_socket.send(message)
        except:
            pass;

setup()