import socket
import threading

host = input("Host name: ")


HOST = socket.gethostbyname(host)
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))
def handle_send():
    while True:
        try:
            mess = input("Message: ")
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
            if data.decode().lower() == "quit":
                client.close()
                break

            print(data.decode())

        except Exception as e:
            client.close()
            print("Client closed!")
            print(e)
            break


send_thread = threading.Thread(target=handle_send, args=())
send_thread.start()

recv_thread = threading.Thread(target=handle_recv, args=())
recv_thread.start()


