import myrsa

# Basis https://tls13.xargs.org
# https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange

# Diffie–Hellman Key Exchange
def dh():
    cpub, cprv = myrsa.generateKeys()  # generate key pair of client
    spub, sprv = myrsa.generateKeys()  # generate key pair of server

    p = cpub[0]
    g = cpub[1]

    a = cprv[0]
    b = sprv[0]

    # Begin
    print("Public:")
    print("p (shared prime)", p)
    print("g (shared base)", g)

    A = (g ** a) % p
    B = (g ** b) % p

    print("\nExchange public:", A)
    print("Exchange public:", B)


    secretA = (B ** a) % p
    secretB = (A ** b) % p

    print("independent shared secret:")
    print("secretA ", secretA)
    print("secretB", secretB)


if __name__ == '__main__':
    dh()

# TODO Next step is implementing this for a client and a server.
