import socket
import threading
import pickle
import os
import sys


def parse_command(message: str) -> dict:
    if message[0] == '/':
        words = message.split(' ')
        command : str = words[0]
        command_body : str = " ".join(words[1:])

        match command:
            case "/quit":
                return {"type": "/quit"}
            
            case _:
                return {"type" : "unreachable"}


def handle_send() -> None:
    while True:
        try:
            mess : str = input("")

            if mess[0] == '/':
                command = parse_command(mess)
                if command["type"] == "unreachable":
                    print("Unknown/unsupported command! Please try again.")
                    continue

                if command["type"] == "/quit":
                    client.sendall(pickle.dumps(command))
                    break
                
                command = pickle.dumps(command)
                client.sendall(command)

            else:
                client.sendall(pickle.dumps({"type": "/message", "text": mess}))
            
        except Exception as e:
            client.close()
            print("Client closed!")
            print(e)
            break


def handle_recv() -> None:
    while True:
        try:
            data : bytes = pickle.loads(client.recv(1024))

            match data["type"]:
                case None:
                    client.close()
                    break

                case "/quit":
                    client.close()
                    break

                case "/message":
                    print(f"{data["user"]} : {data["text"]}")

                case "/user_name":
                    client.sendall(pickle.dumps({"type": "/user_name", "text": user_name}))
                
                case _:
                    client.close()
                    print(f"ERROR: Unknow message type: {data["type"]} received from server")
                    break

        except Exception as e:
            client.close()
            print("Client closed!")
            print(e)
            break


if __name__ == "__main__":

    host : str = ''
    user_name : str = ''
    if len(sys.argv) == 2:
        host = sys.argv[1]

    else:
        host = input("Host name: ")

    user_name = input("Username: ")

    if os.name == "nt":
        os.system("cls")
    else: 
        os.system("clear")
    
    HOST = socket.gethostbyname(host)
    PORT : int = 9090

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}!")

    send_thread = threading.Thread(target=handle_send, args=())
    send_thread.start()

    recv_thread = threading.Thread(target=handle_recv, args=())
    recv_thread.start()


