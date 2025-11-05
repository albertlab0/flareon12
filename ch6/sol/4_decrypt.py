from math import prod
import json

# --- Read primes from factors.txt ---
primes = []
with open("factors.txt", "r") as f:
    for line in f:
        val = line.strip()
        if not val:
            continue
        # Support both decimal and hex (0x...)
        if val.startswith("0x") or val.startswith("0X"):
            primes.append(int(val, 16))
        else:
            primes.append(int(val))

if len(primes) != 8:
    raise ValueError(f"Expected 8 primes, got {len(primes)}")

print("[+] Loaded 8 primes")

# --- Public exponent ---
e = 65537

# --- Compute modulus and phi ---
n = prod(primes)
phi = prod([p - 1 for p in primes])

# --- Modular inverse (extended Euclidean algorithm) ---
def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

def modinv(a, m):
    x, y, g = egcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse")
    return x % m

d = modinv(e, phi)
print("[+] Computed private exponent d")

# --- Decrypt RSA ciphertexts from chat_log.json ---
with open("chat_log.json","r") as f:
    logs = json.load(f)

for idx, entry in enumerate(logs):
    if entry["mode"] == "RSA":
        c_hex = entry["ciphertext"]
        c_bytes = bytes.fromhex(c_hex)

        # ciphertext stored little-endian
        c_int = int.from_bytes(c_bytes, "little")

        # Decrypt: m = c^d mod n
        m_int = pow(c_int, d, n)

        # Convert back to bytes, big-endian
        m_bytes = m_int.to_bytes((m_int.bit_length() + 7) // 8, "big")

        try:
            print(f"[{idx}] {m_bytes.decode()}")
        except UnicodeDecodeError:
            print(f"[{idx}] raw hex: {m_bytes.hex()}")
