import gdb

def u64(bs):
    return int.from_bytes(bs, byteorder="little")

# Notes for testing
# launch pari with debug symbols
# set a breakpoint on znlog
# inspect the past in arguments.

class PrintPariGen(gdb.Command):
    """Read and print 16 bytes of memory at a given address."""

    types_dict = {
          "t_INT"      :  1,
          "t_REAL"     :  2,
          "t_INTMOD"   :  3,
          "t_FRAC"     :  4,
          "t_FFELT"    :  5,
          "t_COMPLEX"  :  6,
          "t_PADIC"    :  7,
          "t_QUAD"     :  8,
          "t_POLMOD"   :  9,
          "t_POL"      :  10,
          "t_SER"      :  11,
          "t_RFRAC"    :  13,
          "t_QFB"      :  15,
          "t_VEC"      :  17,
          "t_COL"      :  18,
          "t_MAT"      :  19,
          "t_LIST"     :  20,
          "t_STR"      :  21,
          "t_VECSMALL" :  22,
          "t_CLOSURE"  :  23,
          "t_ERROR"    :  24,
          "t_INFINITY" :  25
        }
    inv_types_dict = {k:v for (v,k) in types_dict.items()}

    def __init__(self):
        super(PrintPariGen, self).__init__("ppgen", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        # Parse the argument as an address
        address = gdb.parse_and_eval(arg)
        
        # Read 16 bytes from the specified address
        inferior = gdb.selected_inferior()
        gen_type = inferior.read_memory(address, 8)
        type_num = u64(gen_type) >> (64-7)
        print(f'{self.inv_types_dict[type_num]}')

# Register the command with GDB
PrintPariGen()

