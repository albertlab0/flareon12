import idc
import ida_bytes

IMAGE_BASE = 0x140000000

def rename_jump_table_entries():
    """
    Iterates through a large jump table and renames the destination of each entry.
    """
    # --- Configuration ---
    # The starting address of the jump table itself.
    JUMP_TABLE_START_EA = 0x140C687B8 
    
    # The number of entries (cases) in the table.
    NUM_ENTRIES = 65536 
    
    # The size of each entry in the table (in bytes).
    # For a 64-bit binary, this is almost always 8 bytes (a qword).
    # For a 32-bit binary, it would be 4 bytes (a dword).
    ENTRY_SIZE = 4 
    
    # The prefix for the new names.
    NAME_PREFIX = "state"

    print("--- Starting jump table renaming script ---")
    
    renamed_count = 0
    for i in range(NUM_ENTRIES):
        # 1. Calculate the address of the current entry *within* the jump table.
        current_entry_address = JUMP_TABLE_START_EA + (i * ENTRY_SIZE)
        
        # 2. Read the 8-byte pointer from that address. This pointer is the
        #    actual target address of the jump case.
        offs = ida_bytes.get_dword(current_entry_address)
        print(f"offs={offs:x}")
        target_address = offs + IMAGE_BASE
        print(f"target_address={target_address:x}")

        # Check if the read was valid. If the address is invalid or unmapped,
        # get_qword returns BADADDR (-1).
        if target_address == idc.BADADDR or target_address == 0:
            print(f"Warning: Could not read a valid target address at table index {i} (0x{current_entry_address:X}). Skipping.")
            continue
            
        # 3. Construct the new name for the target address.
        #    This will create names like "state0", "state1", etc.
        new_name = f"{NAME_PREFIX}{i}"
        
        # 4. Set the new name at the target address.
        #    This is the equivalent of pressing 'N' in IDA.
        print(f"{target_address:x} -> {new_name}")
        if idc.set_name(target_address, new_name):
            renamed_count += 1
            if i % 1000 == 0: # Print progress every 1000 entries
                print(f"Renamed 0x{target_address:X} to {new_name}")
        else:
            print(f"Warning: Failed to rename address 0x{target_address:X} to {new_name}")
            
    print(f"--- Renaming complete. Total entries renamed: {renamed_count}/{NUM_ENTRIES} ---")

rename_jump_table_entries()
