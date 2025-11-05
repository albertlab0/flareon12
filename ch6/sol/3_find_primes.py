# lcg_prime_generator_s0_inclusive.py
import math
from Crypto.Util.number import long_to_bytes, isPrime



def generate_lcg_primes(m, i, N, seed, count):
    """
    Generates the first 'count' prime numbers from an LCG sequence,
    including the initial seed (s0) in the check.

    Args:
        m (int): The multiplier.
        i (int): The increment.
        N (int): The modulus.
        seed (int): The initial state (s0).
        count (int): The number of prime numbers to find.

    Returns:
        list: A list containing the first 'count' prime numbers.
    """
    primes_found = []
    current_state = seed

    print(f"[*] Starting LCG sequence check with seed s0 = {current_state}")
    print(f"[*] Searching for the first {count} prime numbers...")

    # Set a reasonable limit to prevent infinite loops.
    max_iterations = 10000000

    for seq_index in range(max_iterations):
        # 1. First, check if the CURRENT state is prime.
        #    On the first run (seq_index=0), this will check s0.
        if isPrime(current_state) and current_state.bit_length() == 256:
            primes_found.append(current_state)
            print(f"    Found prime #{len(primes_found)}: {current_state} (from sequence value s{seq_index})")

        # 2. If we have found enough primes, we can stop.
        if len(primes_found) == count:
            return primes_found

        # 3. Only after checking, generate the NEXT state for the next iteration.
        current_state = (m * current_state + i) % N

    # If the loop finishes without finding enough primes
    print(f"\n[!] Warning: Search stopped after {max_iterations} iterations.")
    print(f"    Found {len(primes_found)} of the {count} requested primes.")
    return primes_found


def main():
    """
    Main function to set parameters and run the prime generator.
    """
    # --- PLEASE EDIT THESE VALUES ---
    # Use the parameters you cracked in the previous step.
    # Using the example values from the previous response.
    MODULUS_N = 98931271253110664660254761255117471820360598758511684442313187065390755933409
    MULTIPLIER_M = 11352347617227399966276728996677942514782456048827240690093985172111341259890
    INCREMENT_I = 61077733451871028544335625522563534065222147972493076369037987394712960199707

    # This is the initial state (s0) from your input.txt
    SEED_S0 = 72967016216206426977511399018380411256993151454761051136963936354667101207529
    # --------------------------------

    # The number of prime numbers you want to generate.
    NUM_PRIMES_TO_FIND = 8

    # Generate the primes
    primes = generate_lcg_primes(MULTIPLIER_M, INCREMENT_I, MODULUS_N, SEED_S0, NUM_PRIMES_TO_FIND)

    # Print the final result
    if len(primes) == NUM_PRIMES_TO_FIND:
        print(f"\n[+] Success! The first {NUM_PRIMES_TO_FIND} prime numbers from the sequence are:")
        print(primes)
    else:
        print("\n[-] Could not find the desired number of primes within the iteration limit.")


if __name__ == "__main__":
    main()