import socket
import sys

SERVER = input("Enter server name or IP address: ")

tempPORT = input("Enter port: ")
PORT = int(tempPORT)

if PORT < 0 or PORT > 65535:
    print("Invalid port number.")
    sys.exit()

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except:
    print("Could not connect to server")
    sys.exit()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    #print(client.recv(2048).decode(FORMAT))
    
    #add ACK validation here

#send("Hello world!")
#input()
#send("Hello Everyone!")
#input()
#send("Hello Tim!")
message = input("Enter command: ")
send(message)

send(DISCONNECT_MESSAGE)
client.close()
