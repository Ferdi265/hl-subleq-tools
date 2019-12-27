import sys
from hlsubleq.sim import *

def usage():
    Error("usage: sim.py <file.sbl> [n]")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        usage()

    Asm = create_assembler([SimAssembler, FileInputAssembler])
    asm = Asm(
        infile = sys.argv[1]
    )
    asm.assemble()

    n = None
    if len(sys.argv) == 3:
        n = int(sys.argv[2], 10)

    asm.simulate(n)
