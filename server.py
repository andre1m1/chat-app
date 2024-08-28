import socket
import threading
import logging


HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 9090
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(client_dict):
    client, addr = client_dict["conn"], client_dict["addr"]

    while True:
        try:
            mess = client.recv(1024)
            if mess is None:
                logging.info(f"Client {addr} disconnected!")
                client.close()
                clients.remove(client_dict)
                break

            elif mess.decode() == "quit":
                logging.info(f"Client {addr} disconnected!")
                client.sendall(mess)
                client.close()
                clients.remove(client_dict)
                break
            else:
                logging.info(mess.decode())
                client.sendall(mess)

        except Exception as e:
            client.close()
            clients.remove(client_dict)
            logging.error(f"ERROR: {e} cause by client: {addr}")
            logging.error(f"Client {addr} disconnected!!!")
            break


def main() -> None:
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    server.listen(5)
    logging.info("Server started listening")
    while True:
        client_sock, addr = server.accept()
        logging.info(f"Client: {addr} connected!")
        client = {"id" : len(clients), 
                "conn": client_sock,
                "addr": addr
                }
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, ))
        thread.start()


if __name__ == "__main__":
    main()
