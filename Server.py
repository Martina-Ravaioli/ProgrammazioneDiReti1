import socket as sk
import time

RECV = 4096
SERVER_ADDRESS = ('localhost', 10000)

def  serverMain():

    # Si crea il soket e si associa alla porta
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    sock.bind(SERVER_ADDRESS)

    print ('\n\r starting up on %s port %s' % SERVER_ADDRESS)
    time.sleep(1)
    print ('server ready...')

    message = ''
    exp_num = 0
    ack_sent = 0
    pack_OOO = 0
    rec_pack = 0 


    #il server si mette in ascolto finche non arriva il messaggio END dal client e allora esce
    while True :
        time.sleep(3)
        data,addr = sock.recvfrom(RECV)
        deco_data = data.decode()
        rec_pack = rec_pack + 1
        print(f"Recived package: {deco_data}")
        if deco_data == 'END':
            break
        

        #controlla che il pacchetto sia quello aspettato in base all'ordine
        if int(deco_data) == exp_num : 
            sock.sendto(data, addr)
            ack_sent = ack_sent + 1
            exp_num = exp_num + 1
        #se non è quello aspettato si invia l'ack dell'ultimo pacchetto ricevuto correttamente 
        # così che il client rinvii tutti i pacchetti successivi 
        else : 
            print(f"instead of {exp_num}")
            resend = f"{exp_num - 1}".encode()
            sock.sendto(resend, addr)
            pack_OOO = pack_OOO + 1
            
    sock.close()

    print("\n--- STATISTICS ---")
    print(f"Package recived: {rec_pack}")
    print(f"ACK send: {ack_sent}")
    print(f"Package out of order: {pack_OOO}")
    


serverMain()