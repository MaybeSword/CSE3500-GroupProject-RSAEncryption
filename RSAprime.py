import secrets
import random

# For cryptographic applications, the size should typically be 1024 bits for each prime,
# resulting in a 2048-bit modulus (N). We use a smaller size here for demonstration
# and faster execution in a learning environment.
PRIME_BIT_SIZE = 128
MILLER_RABIN_ROUNDS = 40  # Standard number of iterations for high certainty

def power(a, b, m):
    """
    Computes (a^b) % m efficiently using modular exponentiation (square and multiply).
    This is critical for the speed of the Miller-Rabin test.
    """
    result = 1
    a %= m
    while b > 0:
        # If b is odd, multiply a with result
        if b & 1:
            result = (result * a) % m
        # b must be even now
        a = (a * a) % m
        b //= 2
    return result

def miller_rabin_is_prime(n, k=MILLER_RABIN_ROUNDS):
    """
    Probabilistic primality test: Miller-Rabin.
    Returns True if n is PROBABLY prime, False if n is definitively composite.
    k is the number of rounds, which increases the certainty exponentially.
    """
    # 1. Handle trivial cases
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    # 2. Write n-1 as 2^r * d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # 3. Perform k rounds of testing
    for _ in range(k):
        # Choose a random base 'a' such that 2 <= a <= n - 2
        # We use 'random.randrange' here for speed on very large numbers,
        # but 'secrets' is generally preferred for base generation.
        a = random.randrange(2, n - 2)

        x = power(a, d, n)

        if x == 1 or x == n - 1:
            continue

        # Repeat r-1 times
        for _ in range(r - 1):
            x = power(x, 2, n)
            if x == n - 1:
                break
        else:
            # If the loop finished without finding n-1, n is composite
            return False

    return True

def generate_prime(bits):
    """
    Generates a prime number of the specified bit size using Miller-Rabin testing.
    """
    print(f"-> Generating a {bits}-bit prime...")
    while True:
        # Generate a random number of 'bits' length
        # secrets.randbits is used for cryptographically secure randomness
        candidate = secrets.randbits(bits)

        # Ensure the most and least significant bits are set to 1
        # This guarantees the number is odd and has the correct bit length
        candidate |= (1 << bits - 1) | 1

        # Check for primality
        if miller_rabin_is_prime(candidate):
            return candidate

def generate_rsa_primes(bits=PRIME_BIT_SIZE):
    """
    Generates the two distinct primes, p and q, for RSA.
    """
    p = generate_prime(bits)

    # Ensure q is different from p
    while True:
        q = generate_prime(bits)
        if q != p:
            return p, q

if __name__ == "__main__":
    import time
    start_time = time.time()
    
    # Generate the primes p and q
    p, q = generate_rsa_primes(PRIME_BIT_SIZE)

    # Calculate the modulus N (the public key component)
    n = p * q

    print("\n--- RSA Prime Generation Complete ---")
    print(f"Bit Size per prime: {PRIME_BIT_SIZE}")
    print(f"Total Modulus (N) Bit Size: {n.bit_length()}")
    print("-" * 35)

    print(f"Prime p: {p}")
    print(f"Prime q: {q}")
    print(f"Modulus N (p * q): {n}")
    
    print("-" * 35)
    print(f"Time elapsed: {time.time() - start_time:.4f} seconds")

# EOF marker: Do not remove.
