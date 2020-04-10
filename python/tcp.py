import socket

# Correspondance événements - codes
INITIAL = '0x32'
VITESSE = '0x33'
VITESSE_VAL = 20
MEMOIRE = '0x34'
POS_0 = '0x35'
POS_0_VAL = 20
FEED = '0x36'
DATA = '0x37'
STOP = '0x38'
START = '0x39'
ACK = '0x41'
ERROR = '0x42'


# TCP
HOST = "localhost"
PORT = 12800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print(f"Successfully connected to Arduino on port {PORT}.\n")
except:
    print(f"Failed to connect to Arduino on port {PORT}.\n")



try:
    # INITIALISATION

    # ==== initial ==== #
    s.send(INITIAL)                             # (->) send event
    rcv_initial_evt = s.recv(1024).decode()     # (<-) receive event echo
    assert rcv_initial_evt == ACK, \
           echo_error("initialization", "protocol", "initial",
                      received=rcv_initial_evt,
                      expected=ACK)
                                                # (==) check if event echo same as sent

    # ==== vitesse ==== #
    s.send(VITESSE)                             # (->) send event
    s.send(VITESSE_VAL)                         # (->) send value
    rcv_vitesse_val = s.recv(1024).decode()     # (<-) receive value echo
    assert rcv_vitesse_val == VITESSE_VAL, \
           echo_error("initialization", "value", "vitesse",
                      received=rcv_vitesse_val,
                      expected=VITESSE_VAL)
                                                # (==) check if value echo same as sent

    # ==== memoire ==== #
    rcv_memoire_evt = s.recv(1024).decode()     # (<-) receive event
    assert rcv_memoire_evt == MEMOIRE, \
           echo_error("initialization", "protocol", "memoire",
                      received=rcv_memoire_evt,
                      expected=MEMOIRE)
                                                # (==) check if event echo same as sent
    rcv_memoire_val = s.recv(1024).decode()     # (<-) receive value
    s.send(rcv_memoire_val)                     # (->) send value echo

    # ==== pos_0 ==== #
    s.send(POS_0)                               # (->) send event
    s.send(POS_0_VAL)                           # (->) send value
    rcv_pos_0_val = s.recv(1024).decode()       # (<-) receive value echo
    assert rcv_pos_0_val == POS_0_VAL, \
           echo_error("initialization", "value", "pos_0",
                      received=rcv_pos_0_val,
                      expected=POS_0)
                                                # (==) check if value echo same as sent

except IOError:
    print(f"Connection to peer has been lost.\n")
except InterruptedError:
    print(f"Failed to receive value.\n")
except AssertionError:
    pass
finally:
    print(f"Closing connexion")
    s.close()

def echo_error(protocol_phase, context, variable, received, expected):
    return (
        f"[{protocol_phase.upper()}] Wrong echo ({context}).\n"
        f"Received {variable} of {received} instead of {expected}.\n"
    )
