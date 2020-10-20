import socket
import sys
import subprocess
import time

SERVER = input("Enter server name or IP address: ")

tempPort = input("Enter port: ")
PORT = int(tempPort)

if PORT < 0 or PORT > 65535:
    print("Invalid port number.")
    sys.exit()

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Enter command: ")

index = message.find(">")
textFile = 'writtenFileUDP.txt'

def checkACK():
    try:
        client.settimeout(1)
        ACKmessage, serverADDR = client.recvfrom(2048)
        print(ACKmessage)
        print("after ADK")
        return True
    except socket.timeout:
        print("failed")
        return False

for i in range(3):
    if index > 0:
        length = str(len(message[0:index-1]))
        client.sendto(length.encode(FORMAT), ADDR)
    

        client.sendto(message[0:index-1].encode(FORMAT), ADDR)
        textFile = message[index+2:len(message)]

    else:
        length = str(len(message))
        client.sendto(length.encode(FORMAT), ADDR)
        print("first")

        client.sendto(message.encode(FORMAT), ADDR)
    
    returned = checkACK()
    if returned:
        break
    else:
        if (i == 2):
            print("Failed to send command. Terminating.")
            client.close()
            sys.exit()
        continue
    print("hiola")

modifiedMsg, serverADDR = client.recvfrom(2048)
#print(modifiedMsg.decode(FORMAT))



file1 = open(textFile,"w")
file1.writelines(modifiedMsg.decode(FORMAT))
file1.close()
print("\nFile " + textFile + " saved.")

client.close()
