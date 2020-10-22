#https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
#I based the TCP server and client off of this video, but I changed it up a lot.

#https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
#I learned how to use arguments in the command line using argv from this.

#https://queirozf.com/entries/python-3-subprocess-examples#run-example-store-output-and-error-message-in-string
#I used the example of using run to put the output and error messages into a string.

import socket
import threading
import sys
import subprocess

PORT = sys.argv[1]
ADDR = ('', int(PORT))
FORMAT = 'utf-8'
BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr): #allows for multiple clients to be connected

    #while True:
    msg = conn.recv(BUFFER_SIZE).decode(FORMAT)

    try:        #turns the output or error message into a byte string
        cp = subprocess.run(msg, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        finalMessage = (cp.stdout + cp.stderr).encode(FORMAT)
    except FileNotFoundError as e:
        finalMessage = str(e).encode(FORMAT)

    #try:
    conn.send(finalMessage)
            #break
        #except:
            #continue

    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))  #accepts the new connection and starts a separate thread for each one
        thread.start()

start()