import sys
from Crypto.Cipher import ARC4


key = b'G0ld3n_Tr4nsmut4t10n' 

cipher = b'r2b-\r\x9e\xf2\x1fp\x185\x82\xcf\xfc\x90\x14\xf1O\xad#]\xf3\xe2\xc0L\xd0\xc1e\x0c\xea\xec\xae\x11b\xa7\x8c\xaa!\xa1\x9d\xc2\x90' 

rc4_cipher = ARC4.new(key)
plaintext = rc4_cipher.decrypt(cipher)

with open("flag.out", "wb") as f:
    f.write(plaintext)
