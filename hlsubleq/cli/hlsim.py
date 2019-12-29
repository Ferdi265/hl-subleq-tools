import sys
from hlsubleq.sim import *
from hlsubleq.hlasm import *

def usage():
    Error("usage: {} <file.hlsbl> [n]"
        .format(sys.argv[0])
    )

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        usage()

    Asm = create_assembler([SimAssembler, HlAssembler, FileInputAssembler])
    asm = Asm(
        infile = sys.argv[1]
    )
    asm.assemble()

    n = None
    if len(sys.argv) == 3:
        n = int(sys.argv[2], 10)

    asm.simulate(n)

if __name__ == '__main__':
    main()
