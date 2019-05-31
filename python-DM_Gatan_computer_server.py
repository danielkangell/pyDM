'''
This script is used as a python server run on the Gatan computer to handle IP-based communication between a second computer that controls external hardware and Digital Micrograph. 
'''
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import win32com.client
sys.path.append('pyDM/Win32/Release/') # may need to be modified
import pyDM
import time

pyDM.connect()


while(pyDM.cntMsg() > 0):
    print(pyDM.getMessage()) # clear message buffer. not sure why there's a startup message.



RECEIVE_PORT = 2567
SEND_PORT = 2568
SIZE = 1024

here = gethostbyname( '0.0.0.0' ) # for receiving
external_hardware_computer = '<IP address of external hardware computer>' # for sending

receive_socket = socket( AF_INET, SOCK_DGRAM )
receive_socket.bind( (here, RECEIVE_PORT) )
send_socket = socket( AF_INET, SOCK_DGRAM )

print ("Server listening on port {0}\n".format(RECEIVE_PORT))

while True:
    time.sleep(0.5)
    (script,addr) = receive_socket.recvfrom(SIZE)
    print('Script received:')
    print(repr(script.decode().encode()))
    pyDM.executeScript(script.decode().encode()) # apparently necessary
    message = ""
    while(message == ""):  # wait for script to complete
        time.sleep(0.5)
        message = pyDM.getMessage()
        if(message == 'pyDM0.1_GMS2.1-32bit'):
            message = pyDM.getMessage()
    print(message)
    if(message == "0"): # script completed successfully.
        print('Script execution complete.')
        send_socket.sendto(b'0',(external_hardware_computer,SEND_PORT))
    if(message == "1"): # script was too large
        # print('Script too large.')
        print('Script too long. Please shorten it and try again.')
        send_socket.sendto(b'1',(rop_utem2,SEND_PORT))           

