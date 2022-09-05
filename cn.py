from math import gcd
import secrets
from typing import Tuple

## a)

def are_relatively_prime(e: int, z: int) -> bool:
    """
    Checks if e and z are relatively prime.
    """
    # If two numbers are relatively prime, they have no common factors. So the
    # greatest number that divides both without remainder (the greatest common
    # divisor [gcd]) is 1. So we only need to check that
    return gcd(e, z) == 1

def are_relatively_prime_2(e: int, z: int) -> bool:
    """
    Checks if e and z are relatively prime.
    But this time we won't use the gcd function.
    """
    # We can also check for common factors manually. This implementation
    # is much slower than the one above, but could probably be improved
    # by checking only prime numbers.
    for i in range(2, min(e, z) + 1):
        if e % i == 0 and z % i == 0:
            return False
    return True

## b)

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generates a public and private RSA key pair.
    """
    # First, we need to calculate n, and z using the formulas from the lecture.
    n = p * q
    z = (p - 1) * (q - 1)

    ## Generating a valid e
    # First, set e to a number that is definitely not relatively prime to z.
    e = z
    # Then, select random e in the range [0, n) until it is relatively prime to z.
    while not are_relatively_prime(e, z) or e <= 3:
        e = secrets.randbelow(n)

    ## Searching for a valid d
    # We start with d = 1,
    d = 1
    # and search linearly until we find a d that satisfies the condition shown
    # in the lecture.
    while (e * d) % z != 1:
        d += 1
    return (n, e), (n, d)

def generate_keypair_2(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generates a public and private RSA key pair. Using a more efficient way to calculate d.
    """
    # First, we need to calculate n, and z using the formulas from the lecture.
    n = p * q
    z = (p - 1) * (q - 1)

    ## Generating a valid e
    # First, set e to a number that is definitely not relatively prime to z.
    e = z
    # Select random e in the range [0, n) until it is relatively prime to z.
    while not are_relatively_prime(e, z) or e <= 3:
        e = secrets.randbelow(n)
    
    ## Calculating a valid d
    # The condition from the lecture states, that e d ≡ 1 mod z.
    # Therefore, d is the multiplicative inverse of e in the modulo z ring.
    # We can ask Python to calculate that using the pow function.
    d = pow(e, -1, z)
    return (n, e), (n, d)

## c)

def encrypt(key: Tuple[int, int], m: int) -> int:
    """
    Encrypts a message with a public key.
    """
    # We extract n and e from the key (or if that key is a private key, and we
    # are actually decrypting, n and d.)
    n, e = key
    # Then we just raise m to the e-th power in the modulo n ring, to get the
    # result.
    return pow(m, e, n)

# Decrypting and encrypting is the same operation, so we don't need to repeat it.
# We can just state that the decrypt-function is the same as the encrypt function.
decrypt = encrypt

def encrypt_2(key: Tuple[int, int], m: int) -> int:
    """
    Encrypts a message with a public key but without the much faster pow function.
    
    This solution will be very slow especially for large e or d. So if your
    solution looked like this, you might have noticed that the automatic tests
    took a while.
    """
    # We extract n and e from the key (or if that key is a private key, and we
    # are actually decrypting, n and d.)
    n, e = key
    # Then we just raise m to the e-th power and calculate modulo n, to get the
    # result.
    return m ** e % n
