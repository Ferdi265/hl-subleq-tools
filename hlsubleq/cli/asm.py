import sys
from hlsubleq.asm import *
from hlsubleq.asmext import *

def usage():
    Error("usage: {} <file.sbl> <out> [dryrun] [debug] [raw]"
        .format(sys.argv[0])
    )

def main():
    if len(sys.argv) < 3:
        usage()

    dryrun = False
    debug = False
    raw = False
    for arg in sys.argv[3:]:
        if arg == "dryrun":
            dryrun = True
        elif arg == "debug":
            debug = True
        elif arg == "raw":
            raw = True
        else:
            usage()

    ifaces = [FileInputAssembler]
    if debug:
        ifaces.insert(0, DebugAssembler)
    if not dryrun:
        ifaces.append(FileOutputAssembler)

    Asm = create_assembler(ifaces)
    asm = Asm(
        infile = sys.argv[1], outfile = sys.argv[2], raw = raw
    )

    asm.assemble()
