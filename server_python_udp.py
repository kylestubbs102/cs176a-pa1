import socket
import threading
import sys
import subprocess
import select
from subprocess import check_output
#import time

HEADER = 64
PORT = 5555
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
                try:
                    ACKResentCounter += 1
                    server.settimeout(.5)  #Note: no clear instruction on this
                    msglength, clientADDR = server.recvfrom(2048)
                    continue
                except socket.timeout:
                    break
      
        except socket.timeout:
            print("Failed to receive instructions from the client.")
            failed = True
            break

    
    if msg and not failed and ACKResentCounter < 4:
        msg = msg.decode(FORMAT)
        try:
            cp = subprocess.run(msg, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            finalMessage = (cp.stdout + cp.stderr).encode(FORMAT)
        except FileNotFoundError as e:
            finalMessage = str(e).encode(FORMAT)

        server.sendto(str(len(finalMessage)).encode(FORMAT), clientADDR)


        substringIndex = 0
        ACKResentCounter = 0
        while 479*substringIndex < len(finalMessage):
            startingIndex = (479)*substringIndex  #512-33 = 479
            endIndex = (479)*(substringIndex+1)
            messageChunk = finalMessage[startingIndex:endIndex]
            server.sendto(messageChunk, clientADDR)

            try:
                server.settimeout(1) #No clear instruction here so using 1 second like before
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