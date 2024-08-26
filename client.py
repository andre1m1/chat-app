import socket

host = input("Host name: ")


HOST = socket.gethostbyname(host) 
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))
while True:
    try:
        mess = input("Message: ")
        client.send(mess.encode("utf-8"))
        print(f"Message sent to server: {mess}")

    except:
        client.close()
        print("Client closed!")
        break

client.close()