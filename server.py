import socket
import cryptocode
import myrsa

# Generate a new keypair with our own RSA implementation.
srvKey = myrsa.generateKeys()
srvPublic = srvKey[0]
srvPrivate = srvKey[1]

sharedSecret = None

# Communication function. This will be run when the key exchange is done.
# We receive data continously, decrypt it with the sharedSecret and print it to the terminal.


def coms(conn):
    global sharedSecret
    while True:
        data = conn.recv(1024)
        data = data.decode()
        print(data)  # This prints the encrypted version of the String.
        str_decoded = cryptocode.decrypt(data, sharedSecret)
        print(str_decoded)


def main():
    global sharedSecret
    host = "localhost"  # Our host.
    port = 8304  # Port we listen on.

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()

    print("New connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()

        if not data:
            print('no data received')
            break

        data = str(data)

        print("from client: " + data)

        # On ClientHello we reply with ServerHello. Here we don't send random bytes and don't negotiate algorithms.
        if data == 'ClientHello':
            conn.send("ServerHello".encode())

        # If we receive a public key from the client we calculate our partial result B of the DH key exchange.
        elif data.startswith('key'):
            # 'Parse' the key.
            clTmp = data.replace('key ', '').replace(
                '(', '').replace(')', '').split(', ')

            # Bring key into form: (int, int) where (prime, base)
            clPublic = (int(clTmp[0]), int(clTmp[1]))

            B = (clPublic[1] ** srvPrivate[0]) % clPublic[0]
            print(f'send B: {B}')

            # We send our partial result so the client can calculate the sharedSecret.
            conn.send(f'B {B}'.encode())

        # Receive the clients partial result and calculate the sharedSecret.
        elif data.startswith('A '):
            A = int(data.replace('A ', ''))

            sharedSecret = str((A ** srvPrivate[0]) % clPublic[0])

            print(f'Shared Secret: {sharedSecret}')
            # Start listening for encrypted messages from the client.
            coms(conn)
        else:
            print('Invalid data received: ', data)

    conn.close()  # close the connection when done.


if __name__ == '__main__':
    main()
