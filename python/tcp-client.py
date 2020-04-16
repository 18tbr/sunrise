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

CHAR_SIZE = 1
INT_SIZE = 4


# ------------------------- TCP ------------------------- #
HOST = "localhost"
PORT = 12800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print(f"\n! Successfully connected to Arduino on port {PORT}.\n")
except:
    print(f"\n! Failed to connect to Arduino on port {PORT}.\n")


# --------------- COMMUNICATION FUNCTIONS --------------- #

# BYTE

def send_char(char_value):
    """Send a char"""
    s.send(char_value)
    print(f"[sent] char: {char_value}  (bytes: {CHAR_SIZE})")

def recv_char():
    """Receive a char"""
    char_value = s.recv(CHAR_SIZE)
    print(f"[recv] char: {char_value}  (bytes: {CHAR_SIZE})")
    return char_value

# INT

def send_int(int_value):
    """Send an int"""
    s.send(int_value.to_bytes(INT_SIZE, byteorder=sys.byteorder))
    print(f"[sent] int:  {int_value}    (bytes: {INT_SIZE})")

def recv_int():
    """Receive an int"""
    int_value = int.from_bytes(s.recv(INT_SIZE), byteorder=sys.byteorder)
    print(f"[recv] int:  {int_value}    (bytes: {INT_SIZE})")
    return int_value

# INT VECTOR

# def send_vect(int_vector):
#     """Send an int vector"""
#     s.send(int_value.to_bytes(nb_bytes, byteorder=sys.byteorder))
#     # print(f"[sent] int:  {int_value}    (bytes:   8x{INT_SIZE})")

# def recv_vect():
#     """Receive an int vector"""
#     int_value = int.from_bytes(s.recv(INT_SIZE), byteorder=sys.byteorder)
#     # print(f"[recv] int:  {int_value}    (bufsize: 8x{INT_SIZE})")
#     return int_value


# ------------------------- MAIN ------------------------ #
try:
    ### INITIALIZATION ###
    print("\n### INITIALIZATION ###")

    # ==== initial ==== #
    # Python3    --initial (code 2)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n==== initial ====")
    send_char(INITIAL)                          # (->) send event
    rcv_initial_evt = recv_char()               # (<-) receive event echo
    assert rcv_initial_evt == ACK               # (==) check if event echo same as sent

    # ==== vitesse ==== #
    # Python3    --vitesse (code 3)->    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    print("\n==== vitesse ====")
    send_char(VITESSE)                          # (->) send event
    send_int(VITESSE_VAL)                       # (->) send value
    rcv_vitesse_val = recv_int()                # (<-) receive value echo
    assert rcv_vitesse_val == VITESSE_VAL       # (==) check if value echo same as sent

    # ==== memoire ==== #
    # Python3    <-mémoire (code 4)--    Arduino
    # Python3    <- xxxx (4 octets)--    Arduino
    # Python3    -- xxxx (4 octets)->    Arduino
    print("\n==== memoire ====")
    rcv_memoire_evt = recv_char()               # (<-) receive event
    assert rcv_memoire_evt == MEMOIRE           # (==) check if event echo is protocol
    rcv_memoire_val = recv_int()                # (<-) receive value
    send_int(rcv_memoire_val)                   # (->) send value echo

    # ====  pos_0  ==== #
    # Python3    -- pos_0  (code 5)->    Arduino
    # Python3    -- XXXXXXXX  (vec)->    Arduino
    # Python3    <-  ACK  (code 10)--    Arduino
    print("\n====  pos_0  ====")
    send_char(POS_0)                            # (->) send event
    send_int(POS_0_VAL)                         # (->) send value
    rcv_pos_0_val = recv_int()                 # (<-) receive value echo
    assert rcv_pos_0_val == POS_0_VAL           # (==) check if value echo same as sent

    print("\n### FINISHED ###")


except IOError:
    print(f"! Connection to peer has been lost.\n")
except InterruptedError:
    print(f"! Failed to receive value.\n")
finally:
    print(f"! Closing socket")
    s.close()

