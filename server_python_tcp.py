#https://www.youtube.com/watch?v=3QiPPX-KeSc&ab_channel=TechWithTim
#https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
#https://stackoverflow.com/questions/2502833/store-output-of-subprocess-popen-call-in-a-string
#https://www.geeksforgeeks.org/python-spilt-a-sentence-into-list-of-words/

import socket
import threading
import sys
import subprocess
from subprocess import check_output
#import time

HEADER = 64
PORT = sys.argv[1]
SERVER = ''
ADDR = ('', int(PORT))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" #maybe what ACK is

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):

    connected = True
    while connected: #maybe change to while true
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            #if msg == DISCONNECT_MESSAGE:
            #    connected = False
            #    break

            tempMsg = [msg]
            cmd = tempMsg[0].split()

            #process = subprocess.check_output(cmd, encoding='utf-8')

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            #FOR TESTING
            #time.sleep(.4)
            #conn.send(process.encode(FORMAT))
            try:
                conn.send(output + error)
                break
            except:
                continue

    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
