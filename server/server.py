from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread #multithreaded application so things dont hang for example thread waiting for connections waiting for incoming data etc etc
import time
from person import person


#GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 8000
BUFSIZ =1024
ADDR=(HOST,PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)
MAX_CONNECTIONS=10
BUFSIZ = 1024


#GLOBAL VARIABLES
persons=[]

def broadcast():
    pass

def client_communication(person):
    '''
    Thread to handle all messages from client
    :PARAM client:socket
    :RETURN None
    '''
    client=person.client
    client_address=person.client_address


    #get persons name
    name=client.recv(BUFSIZ).decode('utf8')
    msg=f'{name} has joined the chat'
    broadcast(msg)


    while True:
        msg=client.recv(BUFSIZ)
        if msg ==bytes("{quit}","utf8"):
            client.send(bytes("{quit}","utf8"))
            client.close()
            persons.remove(person)
        else:
        






def wait_for_connection():
    '''
    wait for connection from new clients, start nieuw thread once connected
    :PARAM SERVER:person
    :RETURN: NONE

    '''
    run=True
    while run:
        try:
            """Sets up handling for incoming clients."""
            client, client_address = SERVER.accept()
            person=person(client_address,client)
            persons.append(person)
            print(f'connection{client_address} has connected to the server at {time.time()} ')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print('Failure',e)
            run = False

    print('server has crashed')




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #LISTEN FOR CONNECTIONS
    print("[GESTART ]Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection) # we need a comma here because otherwise its not interpreted as tuple
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()