import socket
import myrsa


srvKey = myrsa.generateKeys()
srvPublic = srvKey[0]
srvPrivate = srvKey[1]


def server_program():
    host = "localhost"
    port = 8303  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            print('no data received')
            break

        print("from connected user: " + str(data))
        
        data = str(data)

        if data == 'ClientHello':
            sendServerHello(conn)
        elif data.startswith('key'): # Calc B and send it.
            clTmp = data.replace('key ', '').replace('(', '').replace(')', '').split(', ')

            clPublic = (int(clTmp[0]), int(clTmp[1]))

            print(clPublic)

            B = (clPublic[1] ** srvPrivate[0]) % clPublic[0]
            print(B)
            conn.send(f'B {B}'.encode())
        else:
            print('Error', data)

        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


def sendServerHello(conn):
    conn.send("ServerHello".encode())


if __name__ == '__main__':
    server_program()
