import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(client_dict):
    client, addr = client_dict["conn"], client_dict["addr"]
    while True:
        try:
            mess = client.recv(1024)

            if not mess:
                print(f"Client {addr} disconnected!")
                client.close()
                clients.remove(client_dict)
                break
            elif mess == "quit":
                print(f"Client {addr} disconnected!")
                client.close()
                clients.remove(client_dict)
                break
            else:
                print(mess.decode())

        except:
            print(f"Client {addr} disconnected!")
            client.close()
            clients.remove(client_dict)
            break


clients = []
server.listen(5)
print(f"Starting server on port: {PORT}")
while True:
    client_sock, addr = server.accept()
    print(f"Client: {addr} connected!")
    client = {"id" : len(clients), 
              "conn": client_sock,
              "addr": addr
              }
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client, ))
    thread.start()

