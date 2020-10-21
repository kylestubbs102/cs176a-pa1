import socket
import sys
import subprocess
import time

#SERVER = input("Enter server name or IP address: ")
SERVER = 'localhost'

#tempPort = input("Enter port: ")
#PORT = int(tempPort)
PORT = 5555

if PORT < 0 or PORT > 65535:
    print("Invalid port number.")
    sys.exit()

HEADER = 64
ACK = 'ACK'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#message = input("Enter command: ")
message = 'dir'

index = message.find(">")
textFile = 'writtenFileUDP.txt'

def checkACK():
    try:
        client.settimeout(1)
        ACKmessage, serverADDR = client.recvfrom(2048)
        return True
    except ConnectionResetError:
        print("Could not connect to server.")
        client.close()
        sys.exit()
    except socket.timeout:
        return False

for i in range(4):
    if index > 0:
        length = str(len(message[0:index-1]))
        client.sendto(length.encode(FORMAT), ADDR)
        client.sendto(message[0:index-1].encode(FORMAT), ADDR)
        textFile = message[index+2:len(message)]

    else:
        length = str(len(message))
        client.sendto(length.encode(FORMAT), ADDR)
        client.sendto(message.encode(FORMAT), ADDR)
    
    returnedACK = checkACK()
    if returnedACK:
        break
    else:
        if (i == 3):
            print("\nFailed to send command. Terminating.")
            client.close()
            sys.exit()
        continue

msgLength, serverADDR = client.recvfrom(2048)
msgLength = int(msgLength.decode(FORMAT))
msgString = b''

previousMessagePacket = b''
didNotReceiveMessagePacketCounter = 0
while msgLength > len(msgString.decode(FORMAT)):   
    try:
        client.settimeout(.5) #No clear instructions for this part so I am using .5 seconds like before
        msgPacket, clientADDR = client.recvfrom(2048)
        client.sendto(ACK.encode(FORMAT), ADDR)
        if (msgPacket != previousMessagePacket):
            previousMessagePacket = msgPacket
        else: #if the length or a packet is resent
            continue
        msgString += msgPacket
    except:
        if didNotReceiveMessagePacketCounter == 3:
            print("\nDid not receive response.")
            client.close()
            sys.exit()
        else:
            didNotReceiveMessagePacketCounter += 1
            continue


file1 = open(textFile,"w")
file1.writelines(msgString.decode(FORMAT))
file1.close()
print("\nFile " + textFile + " saved.")

client.close()
