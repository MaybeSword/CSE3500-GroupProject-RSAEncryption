from typing import Tuple

def power(base: int, exp: int, mod: int) -> int:
    """
    Compute (base ** exp) % mod using square-and-multiply.
    Assumes mod > 1 and exp >= 0.
    """
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
    """
    Thin wrapper around Python's built-in pow(base, exp, mod).
    Keeps the same input checks as `power`.
    """
    if mod <= 1:
        raise ValueError("mod must be > 1")
    if exp < 0:
        raise ValueError("exp must be non-negative")
    return pow(base, exp, mod)

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Iterative extended gcd.
    Returns (g, x, y) with a*x + b*y == g == gcd(a, b).
    """
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modular_inverse(a: int, m: int) -> int:
    """
    Return x such that (a * x) % m == 1.
    Raises ValueError if inverse doesn't exist.
    Uses pow(a, -1, m) when available; otherwise falls back to extended_gcd.
    """
    try:
        return pow(a, -1, m)
    except (TypeError, ValueError):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError("inverse does not exist (not coprime)")
        return x % m

def crt_decrypt(ciphertext: int, d: int, p: int, q: int) -> int:
    """
    Decrypt using Chinese Remainder Theorem.
    Inputs:
      - ciphertext: integer to decrypt
      - d: private exponent
      - p, q: distinct RSA primes
    Steps:
      dP = d mod (p-1)
      dQ = d mod (q-1)
      qInv = q^{-1} mod p
      m1 = ciphertext^{dP} mod p
      m2 = ciphertext^{dQ} mod q
      h = (qInv * (m1 - m2)) mod p
      m = m2 + h * q
    """
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
