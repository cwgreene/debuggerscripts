import gdb

class PrintBigInt(gdb.Command):
    """Read and print 16 bytes of memory at a given address."""

    def __init__(self):
        super(PrintBigInt, self).__init__("printbigint", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        # Parse the argument as an address
        address = gdb.parse_and_eval(arg)
        
        # Read 16 bytes from the specified address
        inferior = gdb.selected_inferior()
        memory = inferior.read_memory(address, 16)


        data_loc_bytes =   inferior.read_memory(address, 8)
        data_loc = int.from_bytes(data_loc_bytes, byteorder='little')
        #print(hex(data_loc))

        length_bytes = inferior.read_memory(address+12, 4)
        length = int.from_bytes(length_bytes, byteorder='little')
        #print(length)

        digits = inferior.read_memory(data_loc, length*8)
        #print(list(digits))
        # Print the memory in a readable format
        print(digits.hex())
        memory_str = int.from_bytes(digits,byteorder="little")
        print(f'{memory_str}')

# Register the command with GDB
PrintBigInt()

