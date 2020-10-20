#https://www.afternerd.com/blog/python-string-contains/
#https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
#https://www.geeksforgeeks.org/reading-writing-text-files-python/
#https://stackoverflow.com/questions/3432102/python-socket-connection-timeout

import socket
import sys
import subprocess #might only need in server

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
    #client.recv(2048).decode(FORMAT)
    
    #add ACK validation here


message = input("Enter command: ")

index = message.find(">")
textFile = 'writtenFileTCP.txt'
if index > 0:
    send(message[0:index-1])
    textFile = message[index+2:len(message)]

else:
    send(message)

try:
    client.settimeout(.5)
    result = client.recv(2048).decode(FORMAT)
except:
    print("\nDid not receive response.")
    sys.exit()
    
    

file1 = open(textFile,"w")
file1.writelines(result)
file1.close()
print("\nFile " + textFile + " saved.")

#send(message)

#send(DISCONNECT_MESSAGE)
client.close()
