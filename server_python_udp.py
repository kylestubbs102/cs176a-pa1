#https://queirozf.com/entries/python-3-subprocess-examples#run-example-store-output-and-error-message-in-string
#I used the example of using run to put the output and error messages into a string.

#https://docs.python.org/3/library/socket.html#socket.socket.settimeout
#I learned how to use settimeout(None), which keeps the server up and prevents it from causing an exception

#https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
#This website helped me create a substring of the string, which helped me send over the file output in separate packets.

#I used the example programs from the textbook to help me familiarize myself with recvfrom() and sendto()

import socket
import sys
import subprocess

PORT = sys.argv[1]
ADDR = ('', int(PORT))
FORMAT = 'utf-8'
ACK = 'ACK'
BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

while True:
    server.settimeout(None)
    failed = False
    msgLength, clientADDR = server.recvfrom(BUFFER_SIZE)

    ACKResentCounter = 0
    while True:
        try: 
            server.settimeout(.5)
            msg, clientADDR = server.recvfrom(BUFFER_SIZE)
            
            if (int(msgLength.decode(FORMAT)) == len(msg.decode(FORMAT))):      #if the message has the same length as the length message sent
                server.sendto(ACK.encode(FORMAT), clientADDR)
                try:
                    ACKResentCounter += 1
                    server.settimeout(.5)  #Note: no clear instruction on this, timeout here to check if ACK is sent again by client
                    msglength, clientADDR = server.recvfrom(BUFFER_SIZE)
                    continue
                except socket.timeout:
                    break
      
        except socket.timeout:
            print("Failed to receive instructions from the client.")
            failed = True
            break

    
    if msg and not failed and ACKResentCounter < 4:
        msg = msg.decode(FORMAT)
        try:        #turns output and error into a byte string
            cp = subprocess.run(msg, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            finalMessage = (cp.stdout + cp.stderr).encode(FORMAT)
        except FileNotFoundError as e:
            finalMessage = str(e).encode(FORMAT)

        server.sendto(str(len(finalMessage)).encode(FORMAT), clientADDR)


        substringIndex = 0
        ACKResentCounter = 0
        while 479*substringIndex < len(finalMessage):           #512-33 = 479, 33 is size of empty byte string
            startingIndex = (479)*substringIndex 
            endIndex = (479)*(substringIndex+1)
            messageChunk = finalMessage[startingIndex:endIndex]
            server.sendto(messageChunk, clientADDR)             #sends several message packets

            try:
                server.settimeout(1) #No clear instruction here so using 1 second like before
                ACKMessage, clientADDR = server.recvfrom(BUFFER_SIZE)       #checks if ACK was sent back
                ACKResentCounter = 0
            except:
                if ACKResentCounter == 3:       #gives up on 3rd try
                    print('File transmission failed.')
                    break
                else:
                    ACKResentCounter += 1
                    continue
            substringIndex += 1