from PIL import Image
from io import BytesIO

# (A) Option 1: If you have the full JPEG hex string (the one you earlier supplied),
# put it here as `jpg_hex` (single long hex string).
jpg_hex = "ffd8ffe000104a46494600010100000100010000ffdb00430001010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101ffc0000b080001002501011100ffc40017000100030000000000000000000000000006040708ffc400241000000209050100000000000000000000000702050608353776b6b7030436747577ffda0008010100003f00c54d3401dcbbfb9c38db8a7dd265a2159e9d945a086407383aabd52e5034c274e57179ef3bcdfca50f0af80aff00e986c64568c7ffd9"

# Convert hex to bytes and open with PIL
jpg_bytes = bytes.fromhex(jpg_hex)
img = Image.open(BytesIO(jpg_bytes))

print("Image size:", img.size, "mode:", img.mode)
# Convert to grayscale/L mode so we get single-byte luminance per pixel
#img_l = img.convert("L")

# Read pixels in row-major order
pixels = list(img.getdata())
print("Pixel count:", len(pixels))
print("Pixel values:", pixels)

# Convert each pixel value to its ASCII character
decoded = ''.join(chr(p) for p in pixels)
print("Decoded string:", decoded)
