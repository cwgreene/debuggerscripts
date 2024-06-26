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

    def lgbits(self, n):

    def print_int(self, addr, header):
        print(f'{self.inv_types_dict[type_num]}')
        print("int")


    def __init__(self):
        super(PrintPariGen, self).__init__("ppgen", gdb.COMMAND_USER)
        self.ptype_dict = {
              "t_INT"      :  lambda x: self.print_int(x),
              "t_REAL"     :  None,
              "t_INTMOD"   :  None,
              "t_FRAC"     :  None,
              "t_FFELT"    :  None,
              "t_COMPLEX"  :  None,
              "t_PADIC"    :  None,
              "t_QUAD"     :  None,
              "t_POLMOD"   :  None,
              "t_POL"      :  None,
              "t_SER"      :  None,
              "t_RFRAC"    :  None,
              "t_QFB"      :  None,
              "t_VEC"      :  None,
              "t_COL"      :  None,
              "t_MAT"      :  None,
              "t_LIST"     :  None,
              "t_STR"      :  None,
              "t_VECSMALL" :  None,
              "t_CLOSURE"  :  None,
              "t_ERROR"    :  None,
              "t_INFINITY" :  None
            }


    def invoke(self, arg, from_tty):
        # Parse the argument as an address
        address = gdb.parse_and_eval(arg)
        
        # Read 16 bytes from the specified address
        inferior = gdb.selected_inferior()
        gen_type = inferior.read_memory(address, 8)
        header = u64(gen_type)
        type_num = header >> (64-7)
        self.ptype_dict[self.inv_types_dict[type_num]](address, header)

# Register the command with GDB
PrintPariGen()

