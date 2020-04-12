import sys
import socket

# Correspondance events - codes
INITIAL = b'2'
VITESSE = b'3'
VITESSE_VAL = 20
MEMOIRE = b'4'
MEMOIRE_VAL = 30
POS_0 = b'5'
POS_0_VAL = 1000
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

# send and receive byte

def send_byte(byte_value):
    """Send a byte"""
    s.send(byte_value)
    print(f"[sent] byte: {byte_value}  (bytes:   1)")

def recv_byte(bufsize):
    """Receive a byte"""
    byte_value = s.recv(bufsize)
    print(f"[recv] byte: {byte_value}  (bufsize: {bufsize})")
    return byte_value

# send and receive int

def send_int(int_value, nb_bytes):
    """Send an int"""
    s.send(int_value.to_bytes(nb_bytes, byteorder=sys.byteorder))
    print(f"[sent] int:  {int_value}    (bytes:   {nb_bytes})")

def recv_int(bufsize):
    """Receive an int"""
    int_value = int.from_bytes(s.recv(bufsize), byteorder=sys.byteorder)
    print(f"[recv] int:  {int_value}    (bufsize: {bufsize})")
    return int_value


# MAIN

try:
    ### INITIALIZATION ###
    print("\n## INITIALIZATION ##")

    # ==== initial ==== #
    # Python3    --initial (code 2)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== initial ====")
    rcv_initial_evt = recv_byte(1)              # (->) receive event
    assert rcv_initial_evt == INITIAL           # (==) check if event is protocol
    send_byte(ACK)                              # (<-) send event echo

    # ==== vitesse ==== #
    # Python3    --vitesse (code 3)->    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    print("\n==== vitesse ====")
    rcv_vitesse_evt = recv_byte(1)              # (->) receive event
    assert rcv_vitesse_evt == VITESSE           # (==) check if event is protocol
    rcv_vitesse_val = recv_int(4)               # (->) receive value
    send_int(rcv_vitesse_val, 4)                # (<-) send value echo

    # ==== memoire ==== #
    # Python3    <-mémoire (code 4)--    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    print("\n==== memoire ====")
    send_byte(MEMOIRE)                          # (<-) send event
    send_int(MEMOIRE_VAL, 4)                    # (<-) send value
    rcv_memoire_val = recv_int(4)               # (->) receive value echo
    assert rcv_memoire_val == MEMOIRE_VAL       # (==) check if value echo same as sent

    # ==== pos_0 ==== #
    # Python3    -- pos_0  (code 5)->    Arduino
    # Python3    -- XXXXXXXX  (vec)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== pos_0 ====")
    rcv_pos_0_evt = recv_byte(1)                # (->) receive event
    assert rcv_pos_0_evt == POS_0               # (==) check if event is protocol
    rcv_pos_0_val = recv_int(1024)              # (->) receive value
    send_int(rcv_pos_0_val, 1024)               # (<-) send value echo

    print("\n## FINISHED ##")


except IOError:
    print(f"! Connection to peer has been lost.\n")
except InterruptedError:
    print(f"! Failed to receive value.\n")
finally:
    print(f"! Closing client")
    s.close()
    print(f"! Closing socket")
    socket.close()

