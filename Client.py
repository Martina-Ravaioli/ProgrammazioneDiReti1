
import socket as sk
import time
import random

TOT = 7
SERVER_ADDRESS = ('localhost', 10000)
RECV = 4096
WINDOW = 3
TIMEOUT = 0.5
PACKET_LOSS_RATE = 0.2

def ClientMain():
        
    # Si crea il soket
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    sent=0
    ack_received=0
    retransmissions=0
    simulated_losses=0

    not_yet_conofirmed_num = 0 
    next_seq_num = 0 

    while not_yet_conofirmed_num < TOT:
        time.sleep(3)
        #i pacchetti vengono inviati finche la finestra non è piena o non sono stati inviati tutti
        while next_seq_num < not_yet_conofirmed_num + WINDOW and next_seq_num < TOT :

            message = f"{next_seq_num}".encode()
        
            #si decide randomicamente se il pacchetto viene preso come simulazione di loss e quindi non viene mandato
            if random.random()<PACKET_LOSS_RATE:
                print(f"Package lost simulation: {next_seq_num}")
                simulated_losses += 1
                sent += 1
            else:
                #se si ricade nel caso senza simulazione di perdita il pacchetto viene inviato
                sock.sendto(message, SERVER_ADDRESS)
                print(f"send package:{next_seq_num}")
                sent += 1
            next_seq_num = next_seq_num + 1 

        try:
            data,addr = sock.recvfrom(4096)
            ack_num = int(data.decode())

            #se l'ack ricevuto è valido si aggiorna il prossimo pacchetto da mandare
            #un ack conferma tutti i pacchetti precedenti
            if ack_num >= not_yet_conofirmed_num:
                print(f"acknowledged package: {ack_num}")
                ack_received = ack_received + 1
                not_yet_conofirmed_num = ack_num + 1
            else : 
            #se è un ack duplicato il client non fa nulla e al primo time out ripare a mandare i pacchetti dall'ultimo confermato 
                print(f"duplicated package: {ack_num}")

        #se non si riceve risposta entro il time out impostato si ricomincia a mandare i messaggi dal primo che non ha ricevuto un ack
        except sk.timeout:
            print(f"there has been a timeout! packages from {not_yet_conofirmed_num} to {next_seq_num-1} will be resent now")
            retransmissions = retransmissions + (next_seq_num - not_yet_conofirmed_num)
            next_seq_num = not_yet_conofirmed_num

    #una volta mandati tutti i pacchetti viene mandato un ultimo pacchetto con messaggio end 
    #per notificare al server che la trasmissione è conclusa 
    sock.sendto("END".encode(), SERVER_ADDRESS)
    print("Finish trasmission")
    #poi si stampano le statistiche relative alla trasmissione
    print("\n--- CLIENT STATISTICS ---")
    print(f"Package sent: {sent}")
    print(f"ACK recived: {ack_received}")
    print(f"Retrasmissions: {retransmissions}")
    print(f"Simulated losses: {simulated_losses}")
    
    sock.close()


ClientMain()