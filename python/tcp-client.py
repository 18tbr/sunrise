import sys
import socket


# ------------------- EVENTS <=> CODES ------------------ #
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


# ------------------------- TCP ------------------------- #
HOST = "localhost"
PORT = 12800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print(f"Successfully connected to Arduino on port {PORT}.\n")
except:
    print(f"Failed to connect to Arduino on port {PORT}.\n")


# --------------- COMMUNICATION FUNCTIONS --------------- #

# BYTE

def send_byte(byte_value):
    """Send a byte"""
    s.send(byte_value)
    print(f"[sent] byte: {byte_value}  (bytes:   1)")

def recv_byte(bufsize):
    """Receive a byte"""
    byte_value = s.recv(bufsize)
    print(f"[recv] byte: {byte_value}  (bufsize: {bufsize})")
    return byte_value

# INT

def send_int(int_value, nb_bytes):
    """Send an int"""
    s.send(int_value.to_bytes(nb_bytes, byteorder=sys.byteorder))
    print(f"[sent] int:  {int_value}    (bytes:   {nb_bytes})")

def recv_int(bufsize):
    """Receive an int"""
    int_value = int.from_bytes(s.recv(bufsize), byteorder=sys.byteorder)
    print(f"[recv] int:  {int_value}    (bufsize: {bufsize})")
    return int_value


# ------------------------- MAIN ------------------------ #
try:
    ### INITIALIZATION ###
    print("\n### INITIALIZATION ###")

    # ==== initial ==== #
    # Python3    --initial (code 2)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== initial ====")
    send_byte(INITIAL)                          # (->) send event
    rcv_initial_evt = recv_byte(1)              # (<-) receive event echo
    assert rcv_initial_evt == ACK               # (==) check if event echo same as sent

    # ==== vitesse ==== #
    # Python3    --vitesse (code 3)->    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    print("\n==== vitesse ====")
    send_byte(VITESSE)                          # (->) send event
    send_int(VITESSE_VAL, 4)                    # (->) send value
    rcv_vitesse_val = recv_int(4)               # (<-) receive value echo
    assert rcv_vitesse_val == VITESSE_VAL       # (==) check if value echo same as sent

    # ==== memoire ==== #
    # Python3    <-mémoire (code 4)--    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    print("\n==== memoire ====")
    rcv_memoire_evt = recv_byte(1)              # (<-) receive event
    assert rcv_memoire_evt == MEMOIRE           # (==) check if event echo is protocol
    rcv_memoire_val = recv_int(4)               # (<-) receive value
    send_int(rcv_memoire_val, 4)                # (->) send value echo

    # ====  pos_0  ==== #
    # Python3    -- pos_0  (code 5)->    Arduino
    # Python3    -- XXXXXXXX  (vec)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n====  pos_0  ====")
    send_byte(POS_0)                            # (->) send event
    send_int(POS_0_VAL, 4)                      # (->) send value
    rcv_pos_0_val = recv_int(1024)              # (<-) receive value echo
    assert rcv_pos_0_val == POS_0_VAL           # (==) check if value echo same as sent

    print("\n### FINISHED ###")


except IOError:
    print(f"! Connection to peer has been lost.\n")
except InterruptedError:
    print(f"! Failed to receive value.\n")
finally:
    print(f"! Closing socket")
    s.close()

