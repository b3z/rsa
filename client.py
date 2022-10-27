import socket
import cryptocode
import myrsa

HOST = "localhost"  # The server's hostname or IP address.
PORT = 8304  # The port used by the server.

# Generate a new keypair with our own RSA implementation.
clKey = myrsa.generateKeys()
clPublic = clKey[0]
clPrivate = clKey[1]

# We can easily pre calculate this for later. 
# This is a calculation step in the Diffie Hellman key exchange.
# See DH-Example.py to see the full exchange we implementated.
A = (clPublic[1] ** clPrivate[0]) % clPublic[0]

sharedSecret = None

# Communication function. This will be run when the key exchange is done.
# It takes commandline input, encrypts it with our sharedSecret. Then sends it to the server.
def coms(s):
    global sharedSecret
    print('\n')
    while True:
        msg = input('> ')
        msg = cryptocode.encrypt(msg, sharedSecret) # For this symmetric encryption we use an external library.
        msg = msg.encode()
        s.sendall(msg)
        print(f'Sent {msg}')
        print('\n')



def main():
    global sharedSecret
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send hello.
        # To make this better send random data to prevent replay attacks.
        # Right now our Hello does not make much sense. Usually we would send version number and negotiable algorithms.
        # We don't because we only support one.
        s.sendall(b"ClientHello")
        print('Sent ClientHello')

        # Here we continously receive data. Responding to incoming data.
        while True:
            data = s.recv(1024)
            data = data.decode()

            print(f'Received {data}')
            input()

            # Send back our pubKey. It is needed for the servers calculations in the DH key exchange.
            if data == 'ServerHello':  
                msg = f'key {clPublic}'
                s.sendall(msg.encode())
                print(f'Sent {msg}')
            
            # B is a partial result from the server we need to calculate the sharedSecret. 
            elif data.startswith('B '):
                B = int(data.replace('B ', ''))

                # Send our A which is our partial result calculated in the very beginning.
                s.sendall(f'A {A}'.encode())
                print(f'Sent A {A}')

                # We gave the server everything it needs to calculate the sharedSecret.
                # Now we calculate it our self.

                sharedSecret = str((B ** clPrivate[0]) % clPublic[0])
                print(f'Shared Secret: {sharedSecret}')

                coms(s) # We are ready to communicate now. So we start doing so.

            else:
                print('Invalid data received: ', data)


if __name__ == '__main__':
    main()
