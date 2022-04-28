import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 1234

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))
server.listen()


print("Server is Listening...")
# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message,client):
    #print(nicknames)

    for inTheArrayclient in clients:
        if (inTheArrayclient != client):
            inTheArrayclient.send(message)




# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)

            broadcast(message,client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            broadcast('{} left!'.format(nickname).encode('ascii'),client)
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
    
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
    
        broadcast("{} joined!\n".format(nickname).encode('ascii'),client)
    
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()