import socket
import threading
import sys

def handle_send():
    while True:
        try:
            mess = input("")
            client.send(mess.encode("utf-8"))

        except Exception as e:
            client.close()
            print("Client closed!")
            print(e)
            break


def handle_recv():
    while True:
        try:
            data = client.recv(1024)
            match data.decode():
                case "quit":
                    client.close()
                    break

                case "user_name":
                    client.send(user_name.encode("utf-8"))
                
                case _:
                    print(data.decode())

        except Exception as e:
            client.close()
            print("Client closed!")
            print(e)
            break


if __name__ == "__main__":

    host = ''
    user_name = ''
    if len(sys.argv) == 2:
        host = sys.argv[1]

    else:
        host = input("Host name: ")

    user_name = input("Username: ")

    HOST = socket.gethostbyname(host)
    PORT = 9090

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    send_thread = threading.Thread(target=handle_send, args=())
    send_thread.start()

    recv_thread = threading.Thread(target=handle_recv, args=())
    recv_thread.start()


