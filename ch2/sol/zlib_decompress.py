#!/usr/bin/env python3
"""
A simple command-line utility to decompress a zlib-compressed file.

Usage:
    python decompress_zlib.py <filename>

This script reads the contents of <filename>, decompresses it using the zlib
library, and saves the result to a new file named <filename>.out.
"""

import zlib
import sys
import os

def decompress_file(input_path):
    """
    Decompresses a file using zlib.

    Args:
        input_path (str): The path to the compressed input file.

    Returns:
        bool: True if successful, False otherwise.
    """
    # Construct the output filename by appending ".out"
    output_path = f"{input_path}.out"

    print(f"[*] Input file:  {input_path}")
    print(f"[*] Output file: {output_path}")

    try:
        # Step 1: Read the compressed data from the input file.
        # It's crucial to open the file in binary read mode ('rb').
        with open(input_path, 'rb') as f_in:
            compressed_data = f_in.read()
        
        print(f"[*] Read {len(compressed_data)} bytes of compressed data.")

        # Step 2: Decompress the data using zlib.
        print("[*] Decompressing...")
        decompressed_data = zlib.decompress(compressed_data)
        
        # Step 3: Write the decompressed data to the output file.
        # It's also crucial to open the output file in binary write mode ('wb').
        with open(output_path, 'wb') as f_out:
            f_out.write(decompressed_data)

        print(f"[*] Wrote {len(decompressed_data)} bytes of decompressed data to {output_path}.")
        print("\n[+] Decompression successful!")
        return True

    except FileNotFoundError:
        print(f"\n[!] Error: The file '{input_path}' was not found.")
        return False
    except zlib.error as e:
        print(f"\n[!] Error: Decompression failed. The file may be corrupt or not zlib-compressed.")
        print(f"    Details: {e}")
        return False
    except PermissionError:
        print(f"\n[!] Error: Permission denied. Could not read '{input_path}' or write to '{output_path}'.")
        return False
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        return False

def main():
    """Main function to handle command-line arguments."""
    # sys.argv is a list containing the script name and command-line arguments.
    # sys.argv[0] is the script name ('decompress_zlib.py')
    # sys.argv[1] will be the filename we provide.
    if len(sys.argv) != 2:
        print("Usage: python decompress_zlib.py <filename>")
        sys.exit(1) # Exit with an error code

    input_filename = sys.argv[1]
    decompress_file(input_filename)

if __name__ == "__main__":
    main()

