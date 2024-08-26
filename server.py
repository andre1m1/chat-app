import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

def handle_client(client, addr):
    while True:
        try:
            mess = client.recv(1024)
            if not mess:
                client.close()
                break
            elif mess == "quit":
                client.close()
                break
            else:
                print(mess.decode(), client)

        except:
            print(f"Client {addr} disconnected!")
            client.close()
            break


server.listen(5)
print(f"Starting server on port: {PORT}")
while True:
    client_socket, address = server.accept()
    print(address)
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()

