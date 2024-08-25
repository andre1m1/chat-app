import socket

HOST = socket.gethostbyname("192.168.100.9") 
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

data = input("Message: ")
client.send(data.encode("utf-8"))
client.close()
