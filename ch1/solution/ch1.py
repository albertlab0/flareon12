def brute_force_flag():
    """
    Iterates through all possible 24-bit keys to find the correct one.
    """
    encoded = b"\xd0\xc7\xdf\xdb\xd4\xd0\xd4\xdc\xe3\xdb\xd1\xcd\x9f\xb5\xa7\xa7\xa0\xac\xa3\xb4\x88\xaf\xa6\xaa\xbe\xa8\xe3\xa0\xbe\xff\xb1\xbc\xb9"
    known_suffix = "flare-on.com"

    # The key is sum >> 8. If sum is 32-bit, the key is 24-bit.
    # The maximum value for a 24-bit key is 2^24 - 1.
    max_key = 2**24

    print(f"[*] Starting brute-force attack on a {max_key} key space...")

    for key in range(max_key):
        # Print progress to show it's working
        if key % 100000 == 0:
            print(f"[*] Trying key: {key}", end='\r')

        plaintext = []
        try:
            for i in range(len(encoded)):
                decrypted_char_code = encoded[i] ^ (key + i)
                # Make sure the result is a valid ASCII character for a flag
                if not (32 <= decrypted_char_code <= 126):
                    break # Not a printable character, probably not the right key
                plaintext.append(chr(decrypted_char_code))
            else: # This 'else' belongs to the for loop, it runs if the loop completes without a 'break'
                flag = ''.join(plaintext)
                if flag.endswith(known_suffix):
                    print("\n[+] Success! Found the correct key.")
                    print(f"[+] Key: {key}")
                    print(f"[+] Flag: {flag}")
                    return # Exit the function once the flag is found
        except Exception:
            # Ignore any errors and continue to the next key
            continue

    print("\n[-] Brute-force finished. Flag not found.")

brute_force_flag()
