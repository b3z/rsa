import random
from math import gcd


def generateRandomPrimes():
    primes = primesInRange(10, 999)
    p = random.choice(primes)
    q = random.choice(primes)
    
    if p == q:
        return generateRandomPrimes()
    else:
        return (p, q)


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False
                
        if isPrime:
            prime_list.append(n)
    return prime_list


def isPrime(e, z):
    return gcd(e, z) == 1

def generateKeys():
    # Generate two different random primes 
    p, q = generateRandomPrimes()
    # p = 5
    # q = 11

    # Calculate RSA Module
    N =  p * q

    # Calculate the euler thing we call z
    z = (p-1)*(q-1)
    
    # Chose e which has to be relative prime to z (1 < e < z)
    e = 0

    for i in range(2, z-1):
        if isPrime(i, z):
            e = i
            break

    # Calculate d
    d = pow(e, -1, z)
    
    # print(f'p={p} q={q} e={e} d={d} N={N}')

    print(f'pub ({e}, {N})')
    print(f'prv ({d}, {N})')

    return ((e, N), (d, N))

def encrypt(m , key):
    # m must be smaller than N
    e = key[0]
    N = key[1]
    return pow(m, e, N)

def decrypt(c, key):
    return encrypt(c, key)

if __name__ == "__main__":
    pub, prv = generateKeys()
    c = encrypt(16, pub)
    print(decrypt(c, prv))
