#https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
#This is the video that I used to learn how to use TCP socket programming. I based the client and the server off of the video, but I made many changes.

#https://www.afternerd.com/blog/python-string-contains/
#I used this website to help me use the find() function, which helped me identify "<" in the middle of the input message.

#https://www.freecodecamp.org/news/how-to-substring-a-string-in-python/
#This website helped me create a substring of the string, which was helpful for sending the command to the left of the "<".

#https://stackoverflow.com/questions/3432102/python-socket-connection-timeout
#This helped me get a grasp on how to set timeouts when a socket is receiving data.

#https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
#This helped me create a while-loop to send a message greater than the buffer without having to send the length first.

#https://www.geeksforgeeks.org/reading-writing-text-files-python/
#I learned how to properly write the string into files from this site.

import socket
import sys

SERVER = input("Enter server name or IP address: ")

tempPORT = input("Enter port: ")
PORT = int(tempPORT)

if PORT < 0 or PORT > 65535:
    print("Invalid port number.")
    sys.exit()

FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
BUFFER_SIZE = 2048

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
except:
    print("Could not connect to server")
    sys.exit()
    
message = input("Enter command: ")

index = message.find(">")
textFile = 'writtenFileTCP.txt'
if index > 0:       #if ">" exists
    client.send(message[0:index-1].encode(FORMAT))
    textFile = message[index+2:len(message)]

else:
    client.send(message.encode(FORMAT))

try:
    currentSize = 0
    sentMessage = b''
    while True:     #loop continues until all the data has been received
        client.settimeout(.5)
        messagePacket = client.recv(BUFFER_SIZE)
        sentMessage += messagePacket
        if len(messagePacket) < BUFFER_SIZE:
            break
    assert(sentMessage != b'')  #check if no message was sent
except:
    print("\nDid not receive response.")
    sys.exit()
    
    
finalResult = sentMessage.decode(FORMAT)
file1 = open(textFile,"w")
file1.writelines(finalResult)
file1.close()
print("\nFile " + textFile + " saved.")

client.close()