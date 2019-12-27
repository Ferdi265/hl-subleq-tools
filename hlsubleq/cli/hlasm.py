import sys
from hlsubleq.hlasm import *

def usage():
    Error("usage: hlasm.py <file.sbl> <out> [dryrun] [debug] [raw]")

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

    ifaces = [HlAssembler, FileInputAssembler]
    if debug:
        ifaces.insert(0, DebugHlAssembler)
    if not dryrun:
        ifaces.append(FileOutputAssembler)

    Asm = create_assembler(ifaces)
    asm = Asm(
        infile = sys.argv[1], outfile = sys.argv[2], raw = raw
    )

    asm.assemble()
