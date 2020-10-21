import socket
import threading
import sys
import subprocess
import select
from subprocess import check_output
#import time

HEADER = 64
PORT = 5556
#PORT = sys.argv[1]
SERVER = ''
ADDR = ('', int(PORT))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" #maybe what ACK is
ACK = 'ACK'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

while True:
    server.settimeout(None)
    failed = False
    msgLength, clientADDR = server.recvfrom(2048)

    ACKResentCounter = 0
    while True:
        try: 
            server.settimeout(.5)
            msg, clientADDR = server.recvfrom(2048)
            
            if (int(msgLength.decode(FORMAT)) == len(msg.decode(FORMAT))):
                server.sendto(ACK.encode(FORMAT), clientADDR)
                #server.setblocking(0)
                try:
                    ACKResentCounter += 1
                    server.settimeout(.5)  #Note: no clear instruction on this
                    msglength, clientADDR = server.recvfrom(2048)
                    continue
                except socket.timeout:
                    break
      
        except socket.timeout:
            print("Failed to receive instructions from the client.")
            #server.setblocking(1)
            failed = True
            break

    
    if msg and not failed and ACKResentCounter < 4:
        msg = msg.decode(FORMAT)
        tempMsg = [msg]
        cmd = tempMsg[0].split()

        try:
            #process = subprocess.check_output(cmd, encoding='utf-8')
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()

        except Exception as e:
            output = str(e).encode(FORMAT)
            error = ''.encode(FORMAT)

        finalMessage = output + error
        print("final message length: ", len(finalMessage))
        print("bytes of finalMessage: ", sys.getsizeof(finalMessage))
        server.sendto(str(len(finalMessage)).encode(FORMAT), clientADDR)


        substringIndex = 0
        #remainingMessageLength = len(finalMessage)

        ACKResentCounter = 0
        #while remainingMessageLength > 0: 
        while 479*substringIndex < len(finalMessage):
            startingIndex = (479)*substringIndex  #512-33 = 479
            endIndex = (479)*(substringIndex+1)
            messageChunk = finalMessage[startingIndex:endIndex]
            server.sendto(messageChunk, clientADDR)

            try:
                server.settimeout(1) #change to 1
                ACKMessage, clientADDR = server.recvfrom(2048)
                ACKResentCounter = 0
            except:
                if ACKResentCounter == 3:
                    print('File transmission failed.')
                    break
                else:
                    ACKResentCounter += 1
                    continue

            substringIndex += 1
            print("messageChunk length: ", len((messageChunk)))
            print("messageChunk bytes: ", sys.getsizeof(messageChunk))     #TOMORROW WORK ON SENDING ACK TO CLIENT, 3 TIMES
            #remainingMessageLength -= len(finalMessage[startingIndex:endIndex])
            #print("remainingMessageLength: ", remainingMessageLength)