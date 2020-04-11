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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print(f"Successfully connected to Arduino on port {PORT}.\n")
except:
    print(f"Failed to connect to Arduino on port {PORT}.\n")


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
    bsend(INITIAL)                              # (->) send event
    rcv_initial_evt = breceive(1)               # (<-) receive event echo
    assert rcv_initial_evt == ACK               # (==) check if event echo same as sent

    # ==== vitesse ==== #
    # Python3    --vitesse (code 3)->    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    print("\n==== vitesse ====")
    bsend(VITESSE)                              # (->) send event
    bsend(VITESSE_VAL)                          # (->) send value
    rcv_vitesse_val = breceive(1024)            # (<-) receive value echo
    assert rcv_vitesse_val == VITESSE_VAL       # (==) check if value echo same as sent

    # ==== memoire ==== #
    # Python3    <-mémoire (code 4)--    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    print("\n==== memoire ====")
    rcv_memoire_evt = breceive(1024)            # (<-) receive event
    assert rcv_memoire_evt == MEMOIRE           # (==) check if event echo is protocol
    rcv_memoire_val = breceive(1024)            # (<-) receive value
    bsend(rcv_memoire_val)                      # (->) send value echo

    # ==== pos_0 ==== #
    # Python3    -- pos_0  (code 5)->    Arduino
    # Python3    -- XXXXXXXX  (vec)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== pos_0 ====")
    bsend(POS_0)                                # (->) send event
    bsend(POS_0_VAL)                            # (->) send value
    rcv_pos_0_val = breceive(1024)              # (<-) receive value echo
    assert rcv_pos_0_val == POS_0_VAL           # (==) check if value echo same as sent



except IOError:
    print(f"Connection to peer has been lost.\n")
except InterruptedError:
    print(f"Failed to receive value.\n")
finally:
    print(f"Closing connexion")
    s.close()

