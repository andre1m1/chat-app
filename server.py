import socket
import threading
import logging

def close_conn(client: dict, with_err: Exception | None = None) -> None:
    conn, addr = client["conn"], client["addr"]
    conn.close()
    try:
        clients.remove(client)
        del conn
        if with_err:
            logging.error(f"ERROR: {with_err} cause by client: {addr}")
            logging.error(f"Client {addr} disconnected!!!")
        else:
            logging.info(f"Client {addr} disconnected!")
            
    except Exception as e:
        logging.error(f"Could not properly close connection: {e}")


def handle_client(client: dict) -> None:
    conn = client["conn"]
    try:
        conn.sendall("user_name".encode("utf-8"))
        user_name = conn.recv(1024).decode()

        client["user_name"] = user_name

    except Exception as e:
        close_conn(client, with_err=e)

    while True:
        try:
            mess = conn.recv(1024).decode()
            if mess is None:
                close_conn(client)
                break

            elif mess == "quit":
                conn.sendall(mess)
                close_conn(client)
                break
            else:
                logging.info(mess)
                mess = f"{client['user_name']} : {mess}"
                for c in clients:
                    c["conn"].sendall(mess.encode())

        except Exception as e:
            close_conn(client, with_err=e)
            break




if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST)
    PORT = 9090
    clients: list[dict] = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    server.listen(5)
    logging.info("Server started listening")
    while True:
        client_sock, addr = server.accept()
        logging.info(f"Client: {addr} connected!")
        client: dict = {
            "id" : len(clients), 
            "conn": client_sock,
            "addr": addr,
            "user_name": None
            }
        clients.append(client)
        client_thread = threading.Thread(target=handle_client, args=(client, ))
        client_thread.start()

