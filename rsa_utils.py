# File: rsa_utils.py
# Description: Contains utility functions for the RSA cryptosystem implementation.

def modular_exponentiation(base, exponent, modulus):
    """
    Performs modular exponentiation (base^exponent) % modulus efficiently.

    This function is a critical component of the RSA algorithm, used for both
    encryption (c = m^e mod n) and decryption (m = c^d mod n). A naive
    approach of calculating base^exponent first and then taking the modulus
    is computationally infeasible for the large numbers used in cryptography.

    This implementation uses the "square-and-multiply" (or binary exponentiation)
    algorithm. This method significantly reduces the number of multiplications
    required by processing the exponent in its binary form. It keeps
    intermediate results small by applying the modulus operator at each step,
    preventing overflow issues and dramatically improving performance.

    Args:
        base (int): The base of the exponentiation.
        exponent (int): The exponent.
        modulus (int): The modulus.

    Returns:
        int: The result of (base^exponent) % modulus.
    """
    # Ensure the modulus is greater than 1, otherwise the operation is trivial or undefined.
    if modulus == 1:
        return 0

    # Initialize result to 1. This will be our accumulator.
    result = 1
    
    # Reduce the base modulo the modulus initially. This helps keep the numbers
    # in all subsequent calculations smaller.
    base = base % modulus

    # Loop as long as the exponent is greater than 0.
    while exponent > 0:
        # If the current least significant bit of the exponent is 1 (i.e., exponent is odd),
        # multiply our current result by the base (and take the modulus).
        # This corresponds to the '1' bits in the binary representation of the exponent.
        if (exponent % 2) == 1:
            result = (result * base) % modulus

        # In each iteration, we halve the exponent (integer division). This is equivalent
        # to right-shifting the bits of the exponent.
        exponent = exponent // 2
        
        # Square the base and take the modulus. This prepares the base for the next
        # bit of the exponent. This is the 'squaring' part of the algorithm.
        base = (base * base) % modulus
    
    # The final result is the accumulated value.
    return result

#Example
# You can use this section to test the function before integrating it.
if __name__ == '__main__':
    # A small example that can be manually verified: 5^117 mod 19
    # 117 in binary is 1110101
    base = 5
    exponent = 117
    modulus = 19
    
    # Expected result is 1
    # 5^1 = 5 mod 19
    # 5^2 = 25 = 6 mod 19
    # 5^4 = 6^2 = 36 = 17 mod 19
    # 5^8 = 17^2 = 289 = 4 mod 19
    # 5^16 = 4^2 = 16 mod 19
    # 5^32 = 16^2 = 256 = 9 mod 19
    # 5^64 = 9^2 = 81 = 5 mod 19
    # 117 = 64 + 32 + 16 + 4 + 1
    # 5^117 = 5^64 * 5^32 * 5^16 * 5^4 * 5^1 mod 19
    #       = (5 * 9 * 16 * 17 * 5) mod 19
    #       = 1 mod 19
    
    result = modular_exponentiation(base, exponent, modulus)
    print(f"Calculation: {base}^{exponent} mod {modulus}")
    print(f"Result: {result}")
    print("-" * 20)

    # A larger example, typical for RSA-like operations
    large_base = 123456789
    large_exponent = 987654321
    large_modulus = 1000000007  # A large prime number

    print("Performing a larger calculation...")
    large_result = modular_exponentiation(large_base, large_exponent, large_modulus)
    print(f"Result of large calculation: {large_result}")