import socket
import cryptocode
import myrsa

HOST = "localhost"  # The server's hostname or IP address
PORT = 8304  # The port used by the server

clKey = myrsa.generateKeys()
clPublic = clKey[0]
clPrivate = clKey[1]

# We can easily pre calculate this for later.
A = (clPublic[1] ** clPrivate[0]) % clPublic[0]

sharedSecret = None

def coms():
    global sharedSecret
    while True:
        # data = s.recvs(1024)
        # data = data.decode()
        # print(data)
        # str_decoded = cryptocode.decrypt(data, sharedSecret)
        # print(str_decoded)
        msg = input('> ')
        msg = cryptocode.encrypt(msg, sharedSecret)
        msg = msg.encode()
        s.sendall(msg)

def handleProtocol(data):
    global sharedSecret
    print(f"Received {data}")
    data = data.decode()
    if data == 'ServerHello':  # Send back our key
        msg = f'key {clPublic}'
        s.sendall(msg.encode())
    elif data.startswith('B '):
        print(data)

        # Parse servers B
        B = int(data.replace('B ', ''))
        # Send our A
        s.sendall(f'A {A}'.encode())
        # calculate sharedSecret
        sharedSecret = str((B ** clPrivate[0]) % clPublic[0])
        print(sharedSecret)
        coms()

    else:
        print('Error', data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Send hello
    # TODO send random data to prevent replay attacks
    s.sendall(b"ClientHello")

    while True:
        data = s.recv(1024)
        handleProtocol(data)
