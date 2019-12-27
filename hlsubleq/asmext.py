from .asm import *

class StringInputAssembler(Assembler):
    def __init__(self, instring, **kwargs):
        super().__init__(**kwargs)
        self.ins = instring

    def read_input(self):
        return self.ins

class FileInputAssembler(Assembler):
    def __init__(self, infile, **kwargs):
        super().__init__(**kwargs)
        self.inf = infile

    def read_input(self):
        with open(self.inf, "r") as infile:
            return infile.read()

class FileOutputAssembler(Assembler):
    def __init__(self, outfile, raw, **kwargs):
        super().__init__(**kwargs)
        self.outf = outfile
        self.raw = raw

    def write_start(self):
        self.outfile = open(self.outf, "w")
        self.cur = None
        self.count = 0
        if not self.raw:
            self.outfile.write("v2.0 raw\n")

    def write_word(self, word):
        def output(word):
            if self.cur != None:
                if self.count > 1:
                    self.outfile.write("{}*{:04x}\n".format(self.count, self.cur))
                else:
                    self.outfile.write("{:04x}\n".format(self.cur))

            self.cur = word
            self.count = 1

        if word == self.cur and not self.raw:
            self.count += 1
        else:
            output(word)

    def write_finish(self):
        self.write_word(None)
        self.outfile.close()

class ArrayOutputAssembler(Assembler):
    def write_start(self):
        self.out_memory = []

    def write_word(self, word):
        self.out_memory.append(word)

    def get_output(self):
        return self.out_memory

class DebugProgram(Program):
    COUNT = 0

    def reset_count(self):
        if self.COUNT != 0:
            print()
            self.COUNT = 0

    def set(self, data, line):
        if self.COUNT == 0:
            print("    ", end = "")

        print(Subleq.to_string(data), end = " ")
        self.COUNT += 1

        if self.COUNT == 3:
            self.COUNT = 0
            print()

        super().set(data, line)

class DebugAssembler(Assembler):
    def __init__(self, **kwargs):
        super().__init__(program = DebugProgram(), **kwargs)

    def parse_label(self, line, token):
        self.program.reset_count()
        print(token)
        super().parse_label(line, token)

    def parse_seek(self, line, token):
        self.program.reset_count()
        print(token)
        super().parse_seek(line, token)

def create_assembler(ifaces):
    class Asm(*ifaces):
        pass

    return Asm
