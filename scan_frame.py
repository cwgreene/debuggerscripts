import gdb
import struct
import colorama

def vmmap():
    result = []
    mappings = gdb.execute("vmmap", from_tty=False, to_string=True).split("\n")
    mappings = [m.split() for m in mappings[1:]]
    for mapping in mappings:
        if len(mapping) < 4:
            continue
        if len(mapping) < 5:
            mapping = mapping + ["?"]
        #print(mapping[0], mapping[1])
        result.append([int(mapping[0], 16), int(mapping[1], 16), mapping[-1]])
    return result

def find_mapping(addr, mappings):
    for mapping in mappings:
        if addr >= mapping[0] and addr <= mapping[1]:
            return mapping[-1]

# TODO: Check out suitability of Frame Decorators
# https://sourceware.org/gdb/onlinedocs/gdb/Frame-Decorator-API.html#Frame-Decorator-API
class ScanCommand(gdb.Command):
    def __init__(self):
        super(ScanCommand, self).__init__("scan_memory", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        # x-64 specific
        bottom_of_stack = int(gdb.parse_and_eval("$rsp"))
        top_of_stack = int(gdb.parse_and_eval("$rbp"))
        args = arg.strip().split(" ") # should do better parsing here
        args = [arg for arg in args if arg != ''] # deal with empty arguments
        if len(args) > 0:
            if len(args) == 1:
                top_of_stack = int(args[0], 16)
            if len(args) == 2:
                bottom_of_stack = int(args[0],16)
                top_of_stack = int(args[1], 16)
        proc = gdb.inferiors()[0]
        mappings = vmmap()
        for i in range((top_of_stack-bottom_of_stack)//8):
            qword = proc.read_memory(bottom_of_stack+8*i, 8)
            value = struct.unpack("Q", qword.tobytes())[0]
            m = find_mapping(value, mappings)
            color = ""
            if m == "[stack]":
                color = colorama.Fore.GREEN
                color += colorama.Style.BRIGHT
            elif m and "libc" in m:
               color = colorama.Fore.RED
               color += colorama.Style.BRIGHT
            print(color + hex(bottom_of_stack+8*i), hex(value), m if m else "", colorama.Fore.RESET, colorama.Style.RESET_ALL)

ScanCommand()
