from typing import Tuple
import secrets
import random

def power(base: int, exp: int, mod: int) -> int:
    if mod <= 1:
        raise ValueError("mod must be > 1")
    if exp < 0:
        raise ValueError("exp must be non-negative")

    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result
    
def mod_pow(base: int, exp: int, mod: int) -> int:
    if mod <= 1:
        raise ValueError("mod must be > 1")
    if exp < 0:
        raise ValueError("exp must be non-negative")
    return pow(base, exp, mod)

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modular_inverse(a: int, m: int) -> int:
    try:
        return pow(a, -1, m)
    except (TypeError, ValueError):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError("inverse does not exist (not coprime)")
        return x % m

def crt_decrypt(ciphertext: int, d: int, p: int, q: int) -> int:
    if p == q:
        raise ValueError("p and q must differ")
    if p <= 1 or q <= 1:
        raise ValueError("invalid prime inputs")

    dP = d % (p - 1)
    dQ = d % (q - 1)
    qInv = modular_inverse(q, p)

    m1 = power(ciphertext, dP, p)
    m2 = power(ciphertext, dQ, q)

    h = (qInv * (m1 - m2)) % p
    m = m2 + h * q
    return m


# ------ Miller–Rabin ------
PRIME_BIT_SIZE = 128
MILLER_RABIN_ROUNDS = 40

def power(a, b, m):
    result = 1
    a %= m
    while b > 0:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b //= 2
    return result

def miller_rabin_is_prime(n, k=MILLER_RABIN_ROUNDS):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = power(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_prime(bits):
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << bits - 1) | 1
        if miller_rabin_is_prime(candidate):
            return candidate

def generate_rsa_primes(bits=PRIME_BIT_SIZE):
    p = generate_prime(bits)
    while True:
        q = generate_prime(bits)
        if q != p:
            return p, q


# -------- RSA KEYGEN/ENCRYPT/DECRYPT WRAPPER --------

def rsa_keygen(bits=128):
    p, q = generate_rsa_primes(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modular_inverse(e, phi)
    return (n, e), (p, q, d)

def rsa_encrypt(m, public_key):
    n, e = public_key
    return power(m, e, n)

def rsa_decrypt(c, private_key):
    p, q, d = private_key
    return crt_decrypt(c, d, p, q)


# -------- Example --------

if __name__ == "__main__":
    pub, priv = rsa_keygen(128)

    message = 123456789
    ciphertext = rsa_encrypt(message, pub)
    recovered = rsa_decrypt(ciphertext, priv)

    print("Message:", message)
    print("Encrypted:", ciphertext)
    print("Decrypted:", recovered)
