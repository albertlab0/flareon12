import json

with open("chat_log.json", "r") as _dump:
    data = json.load(_dump)

values = []

for i in range(7):
    key_num1 = int(data[i]["ciphertext"], 16)
    print(f"\n[+] Ciphertext: {key_num1}")

    key_num2 = data[i]["conversation_time"]
    print(f"[+] Conversation Time: {key_num2}")

    plaintext = data[i]["plaintext"].encode("utf-8")
    padded_plaintext = plaintext.ljust(32, b"\x00")
    print(f"[+] Plaintext: {padded_plaintext}")

    val = key_num1 ^ key_num2 ^ int.from_bytes(padded_plaintext)

    print(f" XOR Val: {val}")
    values.append(val)

with open("input.txt", "w") as f:
    for val in values:
        f.write(f"{val}\n")



