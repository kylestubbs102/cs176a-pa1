import socket
import threading
import sys
import subprocess
import select
from subprocess import check_output
#import time

HEADER = 64
PORT = sys.argv[1]
SERVER = ''
ADDR = ('', int(PORT))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" #maybe what ACK is
ACK = 'ACK'

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

connected = True
while connected: #maybe change to while true
    #msg_length = conn.recv(HEADER).decode(FORMAT)
    #if msg_length:
        #msg_length = int(msg_length)
        #msg = conn.recv(msg_length).decode(FORMAT)
        #if msg == DISCONNECT_MESSAGE:
        #    connected = False
        #    break




    msgLength, clientADDR = server.recvfrom(2048)
    
    server.setblocking(0)
    try: 
        #msg, clientADDR = ready[0][0].recvfrom(2048)
        print("hi")
        server.settimeout(.5)


        msg, clientADDR = server.recvfrom(2048)
        print(int(msgLength.decode(FORMAT)))
        print(len(msg.decode(FORMAT)))
        if (int(msgLength.decode(FORMAT)) == len(msg.decode(FORMAT))):
            print("hola")
            server.sendto(ACK.encode(FORMAT), clientADDR)
            server.setblocking(1)
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        server.setblocking(1)
        continue

    if msg:
        msg = msg.decode(FORMAT)
        tempMsg = [msg]
        cmd = tempMsg[0].split()

        #process = subprocess.check_output(cmd, encoding='utf-8')

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
        except Exception as e:
            print(str(e))
            output = str(e).encode(FORMAT)
            error = ''.encode(FORMAT)


        #FOR TESTING
        #time.sleep(.4)
        #conn.send(process.encode(FORMAT))
    #try:
        server.sendto(output + error, clientADDR)
     #   break
    #except:
     #   continue
