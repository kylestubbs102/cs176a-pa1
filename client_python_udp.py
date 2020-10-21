import socket
import sys
import subprocess
import time

#SERVER = input("Enter server name or IP address: ")
SERVER = 'localhost'

#tempPort = input("Enter port: ")
#PORT = int(tempPort)
PORT = 5556

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
message = 'type server_python_udp.py'

index = message.find(">")
textFile = 'writtenFileUDP.txt'

def checkACK():
    try:
        client.settimeout(100)
        ACKmessage, serverADDR = client.recvfrom(2048)
        #client.setblocking(1)
        print(ACKmessage)
        return True
    except socket.timeout:
        #client.setblocking(1)
        return False

for i in range(4):
    if index > 0:
        length = str(len(message[0:index-1]))
        client.sendto(length.encode(FORMAT), ADDR) #remember to add try-catch around here for initial bind
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
            print("Failed to send command. Terminating.")
            client.close()
            sys.exit()
        continue

msgLength, serverADDR = client.recvfrom(2048)
msgLength = int(msgLength.decode(FORMAT))
print(msgLength)
msgString = b''
didNotReceiveMessagePacketCounter = 0
previousMessagePacket = b''
while msgLength > len(msgString.decode(FORMAT)):   
    try:
        client.settimeout(.5) #change to .5 i think
        msgPacket, clientADDR = client.recvfrom(2048)
        client.sendto(ACK.encode(FORMAT), ADDR)
        #if (int(msgPacket.decode(FORMAT)) == msgLength): #in case length if sent more than once
        #    continue                                       #moved it to else statement
        if (msgPacket != previousMessagePacket):
            previousMessagePacket = msgPacket
        else: #if the length or a packet is resent
            continue
        msgString += msgPacket
        print(len(msgString.decode(FORMAT)))
    except:
        if didNotReceiveMessagePacketCounter == 3:
            print("Did not receive response.")
            client.close()
            sys.exit()
        else:
            didNotReceiveMessagePacketCounter += 1
            continue


#print(modifiedMsg.decode(FORMAT))






#send ACK after you check if all the data was received
print(msgString)
file1 = open(textFile,"w")
file1.writelines(msgString.decode(FORMAT))
file1.close()
print("\nFile " + textFile + " saved.")

client.close()
