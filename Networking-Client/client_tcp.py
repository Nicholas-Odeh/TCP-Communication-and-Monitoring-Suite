# client_tcp_v3: Nicholas
import time  # allows for a update to be timed
import psutil  # PROCESSING SYSTEM UTILITY
import colorama
import socket
import json

colorama.init(autoreset=True)
f_tran_client = ["Send Files"]
no_random = ['Stop', 'Quit', 'n', 'exit', 'quit']

last_rec = psutil.net_io_counters().bytes_recv  # Gives current total amount of bytes recv
last_sent = psutil.net_io_counters().bytes_sent  # Gives total amount of bytes sent
last_total = last_rec + last_sent  # give complete total amount of bytes

gazint_logo = (r"""

               ############        ###        #############  ####   ####     ####   ###############                
             ##############       #####       #############  ####   ######   ####   ###############                
             ####                #######            #####    ####   #######  ####         ###                      
             ####   #######     #### ####         #####      ####   #############         ###                      
             ####   #######    ####   ####       #####       ####   ####  #######         ###                      
             ####      ####   ####     ####    #####         ####   ####   ######         ###                      
              #############  #####      ####  #############  ####   ####     ####         ###                      
                ###########  ####        ###  #############  ####   ###       ###         ###    
                                                    Client

                                                                                                                                   """)

print(f"\033[0;35m{gazint_logo}\033[0m")
print("\n")
# auto hostip finder...for localhost testing only
gethost = socket.gethostbyname(socket.gethostname())  # gets the localhost socket IP
# print (f'Server IP to connect to {gethost}') #visual aid
HOST = gethost  # change this to the IP you want to connect to if not testing on your local machine.
PORT = 5678  # port & host ip must be the same in client and server
print(f" Your Server's IP is  \033[0;32m{HOST}\033[0m, connecting to Port: \033[0;32m{PORT}\033[0m ")  # visual aid

outfit_regen = False
# TCP SOCKET SERVER
while True:  # endless loop
    bytes_rec = psutil.net_io_counters().bytes_recv  # does the same as line 4 -6
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_rec + bytes_sent
    # bandwidth calc
    new_rec = bytes_rec - last_rec
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total
    # 1024->kb / 1024-> mb
    mb_new_rec = new_rec / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024
    # .2f gives .002 | .5f give .00005

    last_rec = bytes_rec
    last_sent = bytes_sent  # new data points for cal to use after each refresh
    last_total = bytes_total

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # connects
        while True:
            client_comment = input("What would you like to tell the server?: ")  # user write string to send to server.
            s.send(client_comment.encode('utf-8'))  # encodes data for transfer.
            response = s.recv(1024).decode('utf-8')  # server response to user packet.
            if client_comment in no_random:
                client_comment = False  # causes an error and shuts down connection.. so I mean it kind of works... LOL
            if client_comment in f_tran_client:
                client_comment = input('what is the location of the file you want to send?')
                print(f' your file is located in \033[0;32m{client_comment}\033[0m')
                send_it = input('Send this file? Enter Y/N here:')
                if send_it == 'Y':
                    print('sending')
            s.send(client_comment.encode('utf-8'))  # encodes data for transfer.
            print(f"{colorama.Fore.RED}{response}")
            print(colorama.Style.RESET_ALL)
            print(
                f' Bandwidth Usage: \033[33m{mb_new_rec:.2f} MB received, {mb_new_sent:.2f} MB send, {mb_new_total:.2f} total usage \033[0m')  # visual for bandwidth
            break
