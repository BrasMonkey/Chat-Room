import socket
from threading import Thread 

host = "localhost"
port = 8080
clients = {}
adresses = {}

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind((host, port))

def broadcast(msg, prefix = ""):
    for client in clients:
        client.sendall(bytes(prefix, "utf8")+ msg)

def handle_client(connection, adress):
    client_name = connection.recv(1024).decode()
    message = "Welcome " + client_name + "! Happy chatting!"
    connection.send(bytes(message, "utf8"))
    broadcast(bytes(client_name + " has joined the room", "utf8"))
    
    clients[connection] = client_name

    while True:
        msg = connection.recv(1024)
        if msg != bytes("/quit", "utf8"):
            broadcast((client_name + ": " + msg.decode("utf8")).encode("utf8"))
        else:
            connection.send(bytes("See you soon!", "utf8"))
            broadcast(bytes(client_name + "has left the room.", "utf8"))
            close_connection(connection)
            print(client_name + "has left")
            break
    
def accept():
    while True:
        connection, adress = sckt.accept()
        print(adress, " has connected")
        connection.send("Welcome! Type your name, please!".encode("utf8"))
        adresses[connection] = adress

        Thread(target=handle_client, args=(connection, adress)).start()

def close_connection(connection):
    connection.sendall(bytes("/quit", "utf8"))
    connection.close()
    del clients[connection]


if __name__ == "__main__":
    sckt.listen(10)
    print("The server is running. 10 slots avaliable")

    thread_1 = Thread(target=accept)
    thread_1.start()
    thread_1.join()