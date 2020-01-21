from __future__ import print_function

import gdb
import string

class PrettyPrintString(gdb.Command):

    # We need this for the decoding of the first character:
    magic = bytes([0x1e])

    # The constant value each charachter is XORed with:
    const = 0xe1

    def __init__(self):
        super (PrettyPrintString, self).__init__("hapra-decode",
                gdb.COMMAND_DATA,
                gdb.COMPLETE_EXPRESSION, True)
        gdb.execute("alias -a hdec = hapra-decode", True)

    def invoke(self, arg, from_tty):
        arg = arg.strip()

        chars = gdb.parse_and_eval(arg)

        # Get the encoded bytestream:
        i = 0
        enc = b''
        while chars[i] != ord("\0"):
            enc += bytes([int(chars[i].cast(gdb.lookup_type("char"))) % 256])
            i += 1

        # Reverse the stream and append the magic number:
        rev = enc[::-1] + self.magic

        # Decode it into a string:
        dec = ""
        for i in range(0, len(rev) - 1):
            dec += chr(rev[i] ^ rev[i+1] ^ self.const)

        # Reverse it again to get the final decoded string:
        print(arg + " \"" + dec[::-1] + "\"")

PrettyPrintString()