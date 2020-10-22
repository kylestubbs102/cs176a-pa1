#https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
#This website helped me create a substring of the string, which was helpful for sending the command to the left of the "<".

#https://www.geeksforgeeks.org/reading-writing-text-files-python/
#I learned how to properly write the string into files from this site.

import socket
import sys

SERVER = input("Enter server name or IP address: ")

tempPort = input("Enter port: ")
PORT = int(tempPort)

if PORT < 0 or PORT > 65535:
    print("Invalid port number.")
    sys.exit()

ACK = 'ACK'
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
BUFFER_SIZE = 2048

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Enter command: ")

index = message.find(">")
textFile = 'writtenFileUDP.txt'

def checkACK(): #checks if ACK was sent from server
    try:
        client.settimeout(1)
        ACKmessage, serverADDR = client.recvfrom(BUFFER_SIZE)
        return True
    except ConnectionResetError: #initially checks if server and port are able to connect
        print("Could not connect to server.")
        sys.exit()
    except socket.timeout:
        return False

for i in range(4):
    if index > 0:   #if "<" exists
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
        if (i == 3):    #fails after 3 retries
            print("\nFailed to send command. Terminating.")
            sys.exit()
        continue

msgLength, serverADDR = client.recvfrom(BUFFER_SIZE)
msgLength = int(msgLength.decode(FORMAT))
msgString = b''

previousMessagePacket = b''
didNotReceiveMessagePacketCounter = 0
while msgLength > len(msgString.decode(FORMAT)):    #loop continues until the client receives the full message
    try:
        client.settimeout(.5)   #No clear instructions for this part so I am using .5 seconds like before
        msgPacket, clientADDR = client.recvfrom(BUFFER_SIZE)
        client.sendto(ACK.encode(FORMAT), ADDR)

        if (msgPacket != previousMessagePacket): #keeps track of the last sent packet to make sure the server didn't resend the same packet
            previousMessagePacket = msgPacket
        else:                   #if the length or a packet is resent
            continue
        msgString += msgPacket

    except:
        if didNotReceiveMessagePacketCounter == 3: #after 3 tries it gives up
            print("\nDid not receive response.")
            sys.exit()
        else:
            didNotReceiveMessagePacketCounter += 1
            continue


file1 = open(textFile,"w")
file1.writelines(msgString.decode(FORMAT))
file1.close()
print("\nFile " + textFile + " saved.")