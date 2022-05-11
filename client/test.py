from http import client
from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread

from sqlalchemy import true

#from server.server import BUFSIZ, HOST


#GLOBAL CONSTANTS


HOST = 'localhost'
PORT = 8000
ADDR = (HOST, PORT)
BUFSIZ =1024

#GLOBAL VAR
messages=[]
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def recieve_messages():
    '''
    receive messages from servers
    :RETURN:None
    '''
    while True:
        try:
            msg=client_socket.recv(BUFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print('Warning',e)
            break


        



def send_message(msg):
    '''
    receive messages from servers
    :PARAM msg: str
    :RETURN:None
    '''
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


        






receive_thread = Thread(target=recieve_messages)
receive_thread.start()

send_message('Bram')
send_message('Hallo World')
