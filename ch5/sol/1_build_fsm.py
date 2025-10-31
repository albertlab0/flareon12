import ida_ua
import ida_funcs
import idautils
import ida_bytes
import ida_frame
import idaapi

import sys

VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"

JUMP_TABLE_START_EA = 0x140C687B8 
NUM_ENTRIES = 65535 
ENTRY_SIZE = 4 


IMAGE_BASE = 0x140000000

def get_jz2_dest(ea):
    if ida_bytes.get_byte(ea) == 0x74:
        offs = ida_bytes.get_byte(ea + 1)
        if offs < 0x80:
            return ea + 2 + offs
    
    else:
        return BADADDR
    

def analyze_state_transit(start_address):
    """
    Analyzes a state machine logic block using the modern IDA API.
    Output will be list of dict:
    e.g.:
    {0:[{'J': 2}, {'U': 3}, {"i": 1}}
   
    """
    print(f"--- Starting analysis at start_address=0x{start_address:x} ---")

    # --- Step 1: Find the initial 'mov' instruction ---
    initial_mov_ea = idaapi.BADADDR
    stack_var_displacement = -1  # We'll store the stack variable's offset/displacement

    SEARCH_INSTRUCTION_COUNT1 = 0x20
    transition_dict = {}
    
    ea = start_address
    mov_addr = BADADDR
    for i in range(SEARCH_INSTRUCTION_COUNT1):
        # Looking for 'mov'
        if idc.print_insn_mnem(ea)== "mov":
            op1 = idc.print_operand(ea, 0)
            op2 = idc.print_operand(ea, 1)
            
            # Check for pattern: mov [rsp + displacement], al
            if op1.startswith("[rsp") and op2 == "al" :
                print(f"Found initial 'mov' instruction at 0x{ea:x}")
                print(f"  -> Stack variable displacement is: {op1}")
                mov_addr = ea
                break
        ea = idc.next_head(ea)
    
    SEARCH_INSTRUCTION_COUNT1 = 0x10
    
    if mov_addr == BADADDR:
        return None
    

    # --- Step 2: Look for all subsequent 'cmp' and 'jz' pairs ---    
    ea = idc.next_head(mov_addr)
    for i in range(SEARCH_INSTRUCTION_COUNT1):
        if idc.print_insn_mnem(ea)== "cmp":
            if idc.get_operand_type(ea, 1) == idc.o_imm:
                val = idc.get_operand_value(ea, 1)
                print(f"val={val:x}")
                assert chr(val) in VALID_CHARS
        
        ea =  idc.next_head(ea)   
        if ida_bytes.get_byte(ea) == 0x74:  # jz
            jz_dst = get_jz2_dest(ea)
            print(f"jz_dst={jz_dst:x}")
            
            # expected instruction mov     [rsp+59398h+state], 2
            if idc.print_insn_mnem(jz_dst) == "mov":
                op1 = idc.print_operand(jz_dst, 0)
                if op1.startswith("[rsp"):
                    state = idc.get_operand_value(jz_dst, 1)
                    assert state <= 0x20000
                    print(f"state={state}")
                    transition_dict[chr(val)] = state
                    
        # stop at jmp instruction
        if ida_bytes.get_byte(ea) == 0xeb:
            break
    return transition_dict

def main():    
    with open("fsm_tranistion.txt", "w") as f:
        for state in range(NUM_ENTRIES):
            current_entry_address = JUMP_TABLE_START_EA + (state * ENTRY_SIZE)
            offs = ida_bytes.get_dword(current_entry_address)
            # print(f"offs={offs:x}")
            target_address = offs + IMAGE_BASE
            
            dic = analyze_state_transit(target_address)
            if dic:
                for k, v in  dic.items():
                    f.write(f"{state},{k},{v}\n")

main()
    


