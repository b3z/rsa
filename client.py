import myrsa

# Basis https://tls13.xargs.org

def hello():
    cpub, cprv = myrsa.generateKeys() # generate key pair of client
    spub, sprv = myrsa.generateKeys() # generate key pair of server

    # xpub = cpub[0] * spub[1]
    # ypub = cpub[1] * spub[0]
    
    xk = cpub * sprv 

    print(cpub)
    print(spub)
    print('')
    print(xk)
    
    # print(xpub)
    # print(ypub)

def ecm(x, y)
    



if __name__ == '__main__':
    hello()

    

