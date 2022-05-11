from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread #multithreaded application so things dont hang for example thread waiting for connections waiting for incoming data etc etc
import time
from person import Person


#GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 8000
BUFSIZ =1024
ADDR=(HOST,PORT)
MAX_CONNECTIONS=10
BUFSIZ = 1024


#GLOBAL VARIABLES
persons=[]
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR) #setup server

def broadcast(msg,name):
    '''
    sends new messages to all clients
    :PARAM msg: bytes['utf8']
    :PARAM name: str
    :RETURN:None
    '''
    for person in persons:
        client = person.client
        client.send(bytes(name,'utf8') + msg)

def client_communication(person):
    '''
    Thread to handle all messages from client
    :PARAM person:person
    :RETURN None
    '''
    print(person)
    client = person.client
    #get persons name
    name=client.recv(BUFSIZ).decode('utf8')
    msg=bytes(f"{name} has joined the chat",'utf8')
    broadcast(msg,'') #broadcast welcome message


    while True:
        try:
            msg=client.recv(BUFSIZ)
            print(f'{name}:', msg.decode('utf8'))
            if msg ==bytes("{quit}","utf8"):
                broadcast(f'{name} has left the chat at {time.time()}','')
                client.send(bytes("{quit}","utf8"))
                client.close()
                persons.remove(Person)
                break
            else:
                broadcast(msg,name+': ')
        except Exception as e:
            print("WARNING",e)
            break
 

        






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
            #print(client,client_address)
            person=Person(client_address,client)
            persons.append(person)
            print(person)
            print(f'connection{client_address} has connected to the server at {time.time()} ')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print('Warning',e)
            run = False

    print('server has crashed')




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #LISTEN FOR CONNECTIONS
    print("[GESTART ]Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection,) # we need a comma here because otherwise its not interpreted as tuple
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()