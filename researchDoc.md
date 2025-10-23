# RSA (Rivest–Shamir–Adleman) Encryption

- **Asymmetric cryptosystem** → uses public key (encrypt) and private key (decrypt)
- Security relies on the difficulty of factoring the product of two large primes.
- Common uses: secure key exchange, digital signatures, TLS encryption
- Core equations:  
  - Encryption: `c = m^e mod n`  
  - Decryption: `m = c^d mod n`


## Week 1: Mathematical Foundations

- Reviewed **prime numbers**, **modular arithmetic**, **Euler’s totient function**
- Key equations:  
  - `n = p × q`  modulus
  - `φ(n) = (p - 1)(q - 1)` Euler’s totient
  - p and q are large prime numbers; Choose p, q ∈ ℙ such that both are large and distinct

- RSA key generation steps:
  1. Pick large primes `p`, `q`
  2. Compute `n` and `φ(n)`
  3. Choose `e` where `gcd(e, φ(n)) = 1`
  4. Compute `d` as modular inverse of `e`
- Public key → `(n, e)`  
- Private key → `(n, d)`
- Main takeaway: factoring `n` is extremely hard → foundation of RSA’s security


## Week 2: Encryption, Decryption & Padding

- Verified encryption/decryption as modular inverses:
  - **Encryption:** `c = m^e mod n`
  - **Decryption:** `m = c^d mod n`
- Learned that without padding, RSA is deterministic → vulnerable to replay and chosen-plaintext attacks


## Week 3: Security & Comparisons

- Explored vulnerabilities:
  - Weak prime selection → easy factorization
  - Timing / side-channel attacks
  - Chosen ciphertext attacks (CCA)
  - Key reuse or exposure
- Compared with other cryptosystems:

  | System | Mathematical Basis | Security | Efficiency |
  |---------|--------------------|-----------|-------------|
  | **RSA** | Integer factorization | Strong (classical) | Moderate |
  | **ECC** | Elliptic curve discrete log | Stronger, smaller keys | Fast |
  | **Diffie–Hellman** | Discrete logarithm | Secure for key exchange | Moderate |

- Quantum threat: **Shor’s algorithm** can factor large numbers efficiently → breaks RSA
- Best practices: use ≥2048-bit keys, OAEP padding, and hybrid encryption (RSA + symmetric)


## Time and Space Complexity

- **Key Generation:**  
  - Generates large primes and modular inverses  
  - **Time Complexity:** `O((log n)^4)`  
  - **Space Complexity:** `O(log n)` (for storing big integers)

- **Encryption:**  
  - Modular exponentiation via fast exponentiation  
  - **Time Complexity:** `O((log n)^3)`  
  - **Space Complexity:** `O(log n)`

- **Decryption:**  
  - Uses private exponent `d`, can be optimized with CRT  
  - **Time Complexity:** `O((log n)^3)` (≈ half with CRT)  
  - **Space Complexity:** `O(log n)`

- **Overall:**  
  RSA is computationally intensive but highly secure for moderate data sizes.  
  ECC offers similar strength with smaller keys and lower computational cost.


## Summary

- RSA relies on prime factorization hardness and modular arithmetic.  
- Key generation is the most expensive step; encryption and decryption are manageable but slower than symmetric systems.  
- Security depends on key size, random prime selection, and proper padding.  
- RSA remains a cornerstone of modern cryptography but faces challenges from quantum computing and the rise of more efficient systems like ECC.  
- Overall: RSA is secure, proven, and foundational, but gradually being replaced by faster, quantum-resistant methods in practice.



## Works Cited

"PKCS #1: RSA Cryptography Specifications Version 2.2." *RFC 8017*, Internet Engineering Task Force (IETF), Nov. 2016, https://www.rfc-editor.org/rfc/rfc8017.

Rivest, Ronald L., Adi Shamir, and Leonard Adleman. "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems." *Communications of the ACM*, vol. 21, no. 2, Feb. 1978, pp. 120–126. https://doi.org/10.1145/359340.359342.

"RSA Cryptosystem." *Khan Academy*,https://www.khanacademy.org/computing/computer-science/cryptography/modern-crypt/v/intro-to-rsa-encryption.
