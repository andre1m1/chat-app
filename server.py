import socket
import threading
import pickle
import logging

type Err = Exception | None
type Client = dict[str, socket.socket | str | int]
type Clients = list[Client]

def close_conn(client: Client, with_err: Err = None) -> None:
    conn: socket.socket = client["conn"]
    addr = client["addr"]
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



def handle_client(client: Client) -> None:
    conn: socket.socket = client["conn"]
    try:
        conn.sendall(pickle.dumps({"type": "/user_name"}))

        client_mess = pickle.loads(conn.recv(1024))
        if client_mess["type"] != "/user_name":
            raise RuntimeError("Could not receive proper '/user_name' message from client")
        
        user_name : str | None = client_mess["text"]
        if user_name is None:
            raise RuntimeError("Could not receive proper '/user_name' message from client")

        client["user_name"] = user_name

    except Exception as e:
        close_conn(client, with_err=e)

    while True:
        try:
            client_mess = pickle.loads(conn.recv(1024))

            match client_mess["type"]:
                case None:
                    close_conn(client)
                    break

                case "/quit":
                    conn.sendall(pickle.dumps(client_mess))
                    close_conn(client)
                    break

                case "/vote":
                    vote_body : list[str] = client_mess["body"].split(' ')
                    vote_type : str = vote_body.pop(0)
        
                    logging.info(vote_type)
                    if vote_type == "kick":
                        if len(vote_body) > 1:
                            conn.sendall(pickle.dumps({"type": "/unreachable"}))
                        
                        user_name = vote_body.pop()
                        user : Client | None = None
                        for client in clients:
                            if client["user_name"] == user_name:
                                user = client
                                break
                        
                        if user == None:
                            conn.sendall(pickle.dumps({"type": "/unreachable"}))
                        
                        user["kick"] += 1
                        if user["kick"] >= len(clients) / 2:
                            user["conn"].sendall(pickle.dumps({"type" : "/quit"}))
                            close_conn(user)
                    else:
                        conn.sendall(pickle.dumps({"type": "/unreachable"}))

                case "/message":
                    logging.info(client_mess)
                    message : dict[str, str] = {
                        "type": "/message",
                        "user": client["user_name"],
                        "text": client_mess["text"]
                    }

                    for c in clients: 
                        c["conn"].sendall(pickle.dumps(message))
                
                    continue
                case _:
                    close_conn(client)
                    print(f"ERROR: Unknow message type: {client_mess["type"]} received from client: {client}")
                    break



        except Exception as e:
            close_conn(client, with_err=e)
            break




if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST)
    PORT : int = 9090

    clients: Clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    server.listen(5)
    logging.info("Server started listening")
    while True:
        client_sock, addr = server.accept()
        logging.info(f"Client: {addr} connected!")
        client: Client = {
            "id" : len(clients), 
            "conn": client_sock,
            "addr": addr,
            "user_name": "",
            "kick": 0
            }
        clients.append(client)
        client_thread = threading.Thread(target=handle_client, args=(client, ))
        client_thread.start()

