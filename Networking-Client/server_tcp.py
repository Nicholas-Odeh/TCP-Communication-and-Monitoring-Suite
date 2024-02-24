#server_tcp_v3: Nicholas
import time  #allows for a update to be timed
import psutil #PROCESSING SYSTEM UTILITY
import colorama
import socket
import json
colorama.init(autoreset=True)
filename = 'comms_log.json'
spacer = '|---|'



last_rec = psutil.net_io_counters().bytes_recv  #Gives current total amount of bytes recv
last_sent = psutil.net_io_counters().bytes_sent #Gives total amount of bytes sent
last_total = last_rec + last_sent #give complete total amount of bytes

gazint_logo = (r"""

               ############        ###        #############  ####   ####     ####   ###############                
             ##############       #####       #############  ####   ######   ####   ###############                
             ####                #######            #####    ####   #######  ####         ###                      
             ####   #######     #### ####         #####      ####   #############         ###                      
             ####   #######    ####   ####       #####       ####   ####  #######         ###                      
             ####      ####   ####     ####    #####         ####   ####   ######         ###                      
              #############  #####      ####  #############  ####   ####     ####         ###                      
                ###########  ####        ###  #############  ####   ###       ###         ###    
                                                    Server

                                                                                                                                   """)

print(f"\033[0;35m{gazint_logo}\033[0m")
print("\n")




#auto hostip finder...for localhost testing only
gethost = socket.gethostbyname(socket.gethostname())
print (f'This is your host IP for your server:\033[0;32m  {gethost} \033[0m') #visual aid
HOST = gethost #No need to change this.
PORT = 5678  #port must be same in client and server

#TCP SOCKET SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT)) #binds host and port to the server being made
print( f' \n \033[0;31m          ///Binding Server//// \033[0m' )
print(f'Host binded to:\033[0;32m {HOST}\033[0m Port binded to: \033[0;32m{PORT}\033[0m')  #visual aid
print( f'  \033[0;31m          ///Binding Done//// \033[0m' )
print (f'\n')


server_response = ("   PACKET RECEIVED |  SYN/ACK    ")  #server responses...only SYN/ACK enabled for now.
server_response_3 = ("   SERVER ERROR.. Try again later. ")  #Not in use
server.listen(5) #limits  connects allowed....more than 5 connnects = reject

while True: #endless loop
    bytes_rec = psutil.net_io_counters().bytes_recv  #does the same as line 4 -6
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total =  bytes_rec +  bytes_sent
#bandwidth calc |  1024->kb / 1024-> mb
    new_rec = bytes_rec - last_rec
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    mb_new_rec = new_rec / 1024  / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024
    #.2f gives .002 | .5f give .00005

    last_rec = bytes_rec
    last_sent = bytes_sent  #new data points for cal to use after each refresh
    last_total = bytes_total


    comms_socket, address = server.accept()  #comms socket used to talk to client.
    print(f' Client Connection Int:\033[0;31m SYN \033[0m') #visual for connection with client
    message = comms_socket.recv(1024).decode('utf-8') #Message from client is decoded and buffered for bits
    print (f' Client message:\033[0;32m {message} \033[0m ') #clients message displayed
    print ( f' Bandwidth Usage: \033[33m{mb_new_rec:.2f} MB received, {mb_new_sent:.2f} MB send, {mb_new_total:.2f} total usage \033[0m')#visual for bandwidth | .2f=.002 | .5f=.00005
    with open(filename, 'a') as f: #appends to json file
        json.dump(message,f, indent=4)
        json.dump(spacer,f, indent=4)
        print (f' \033[0;35mData saved\033[0m'),
    comms_socket.send((server_response).encode('utf-8'))  #encodes server's SYN/ACK response.
    comms_socket.close() #closes the connection between the client and server. Ends the program.

