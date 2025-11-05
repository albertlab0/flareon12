# lcg_cracker.py
import math
from functools import reduce


def crack_lcg(states):
    """
    Recovers the parameters (m, i, N) of an LCG from a sequence of its outputs.
    The LCG is in the form: S(n+1) = (m * S(n) + i) mod N
    """
    if len(states) < 5:
        print("[!] Error: Not enough states provided. Need at least 5 to reliably determine the parameters.")
        return None, None, None

    # 1. Calculate the differences between consecutive states
    # d(n) = S(n+1) - S(n)
    diffs = [s2 - s1 for s1, s2 in zip(states, states[1:])]

    # 2. Calculate the zero-terms T(n) = d(n+1)^2 - d(n)*d(n+2)
    # These terms must all be multiples of the modulus N.
    zero_terms = [d2 * d2 - d1 * d3 for d1, d2, d3 in zip(diffs, diffs[1:], diffs[2:])]

    # 3. Find the modulus N by taking the GCD of the zero-terms.
    # N must divide all zero_terms, so it must divide their GCD.
    # In a CTF, N is almost always the absolute value of this GCD.
    modulus_N = abs(reduce(math.gcd, zero_terms))

    if modulus_N == 0:
        print("[!] Error: Calculated modulus is zero. Cannot proceed.")
        return None, None, None

    # 4. Find the multiplier m using d(1) = m * d(0) (mod N)
    # m = d(1) * modInverse(d(0)) mod N
    # This requires Python 3.8+ for the pow(base, -1, mod) syntax.
    try:
        inv_d0 = pow(diffs[0], -1, modulus_N)
    except ValueError:
        print(f"[!] Error: Modular inverse of {diffs[0]} (mod {modulus_N}) does not exist.")
        print("    This can happen if the difference and the modulus share a common factor.")
        return None, None, None

    multiplier_m = (diffs[1] * inv_d0) % modulus_N

    # 5. Find the increment i using S(1) = (m * S(0) + i) mod N
    # i = S(1) - m * S(0) mod N
    increment_i = (states[1] - multiplier_m * states[0]) % modulus_N

    return multiplier_m, increment_i, modulus_N


def main():
    """
    Main function to read input and run the cracker.
    """
    try:
        with open('input.txt', 'r') as f:
            # Read states from the file, converting each line to an integer
            states = [int(line.strip()) for line in f if line.strip()]

        print(f"[*] Read {len(states)} states from input.txt")
        m, i, N = crack_lcg(states)

        if m is not None:
            print("\n[+] Success! Found LCG parameters:")
            print(f"    Modulus (N)     : {N}")
            print(f"    Multiplier (m)  : {m}")
            print(f"    Increment (i)   : {i}")

            # Verification step
            print("\n[*] Verifying parameters...")
            s_next = (m * states[0] + i) % N
            if s_next == states[1]:
                print("    Verification successful: (m*S(0) + i) % N == S(1)")
            else:
                print("    Verification failed.")

    except FileNotFoundError:
        print("[!] Error: input.txt not found. Please create it and add the LCG states.")
    except ValueError:
        print("[!] Error: input.txt contains non-integer values.")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()