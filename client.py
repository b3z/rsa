import socket
import myrsa

HOST = "localhost"  # The server's hostname or IP address
PORT = 8303  # The port used by the server

clKey = myrsa.generateKeys()
clPublic = clKey[0]
clPrivate = clKey[1]


def handleProtocol(data):
    print(f"Received {data}")
    data = data.decode()
    if data == 'ServerHello':  # Send back our key
        msg = f'key {clPublic}'
        s.sendall(msg.encode())
    elif data.startswith('B '):
        print(data)
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
