import socket

# Correspondance events - codes
INITIAL = b'2'
VITESSE = b'3'
VITESSE_VAL = b'20'
MEMOIRE = b'4'
MEMOIRE_VAL = b'30'
POS_0 = b'5'
POS_0_VAL = b'40'
FEED = b'6'
DATA = b'7'
STOP = b'8'
START = b'9'
ACK = b'a'
ERROR = b'b'


# TCP
HOST = "localhost"
PORT = 12800
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(10)
print(f"Listening on port {PORT}")
try:
    s, infos_connexion = socket.accept()
    print(f"Successfully connected to Python3 on port {PORT}.\n")
except:
    print(f"Failed to connect to Python3 on port {PORT}.\n")


# COMMUNICATION FUNCTIONS

def bsend(value):
    """Send a value and print it"""
    s.send(value)
    print(f"[sent] value: {value}")

def breceive(bufsize):
    """Receive a value and print it"""
    value = s.recv(bufsize)
    print(f"[received] value: {value}")
    return value


# MAIN

try:
    ### INITIALIZATION ###

    # ==== initial ==== #
    # Python3    --initial (code 2)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== initial ====")
    rcv_initial_evt = breceive(1)               # (->) receive event
    assert rcv_initial_evt == INITIAL           # (==) check if event is protocol
    bsend(ACK)                                  # (<-) send event echo

    # ==== vitesse ==== #
    # Python3    --vitesse (code 3)->    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    print("\n==== vitesse ====")
    rcv_vitesse_evt = breceive(1024)            # (->) receive event
    assert rcv_vitesse_evt == VITESSE           # (==) check if event is protocol
    rcv_vitesse_val = breceive(1024)            # (->) receive value
    bsend(rcv_vitesse_val)                      # (<-) send value echo

    # ==== memoire ==== #
    # Python3    <-mémoire (code 4)--    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    print("\n==== memoire ====")
    bsend(MEMOIRE)                              # (<-) send event
    bsend(MEMOIRE_VAL)                          # (<-) send value
    rcv_memoire_val = breceive(1024)            # (->) receive value echo
    assert rcv_memoire_val == MEMOIRE_VAL       # (==) check if value echo same as sent

    # ==== pos_0 ==== #
    # Python3    -- pos_0  (code 5)->    Arduino
    # Python3    -- XXXXXXXX  (vec)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== pos_0 ====")
    rcv_pos_0_evt = breceive(1024)              # (->) receive event
    assert rcv_pos_0_evt == POS_0               # (==) check if event is protocol
    rcv_pos_0_val = breceive(1024)              # (->) receive value
    bsend(rcv_pos_0_val)                        # (<-) send value echo



except IOError:
    print(f"Connection to peer has been lost.\n")
except InterruptedError:
    print(f"Failed to receive value.\n")
finally:
    print(f"Closing connexion")
    s.close()
    socket.close()

