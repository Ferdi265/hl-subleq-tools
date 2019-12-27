from functools import reduce
from .asm import *
from .asmext import *

class HlToken(Token):
    instructions = [
        "SUBLEQ",
        "SUB",
        "MOVNEG",
        "MOV",
        "ADD",
        "CLEAR",
        "LDI",
        "STI",
        "JMP",
        "JLEZ",
        "JGEZ",
        "JEQM",
        "JEQZ",
        "JLE",
        "JGE",
        "JLT",
        "JGT",
        "JEQ",
        "JAL",
        "JR",
        "HLT"
    ]

    def is_symbol(self, token):
        return super().is_symbol(token) and token not in self.instructions

class HlAssembler(Assembler):
    ZERO = "_ZERO"
    ONE = "_ONE"
    HALTADDR = "_HALT"
    TEMPS = ["_TEMP0", "_TEMP1", "_TEMP2"]

    LDICOUNT = 0
    STICOUNT = 0

    JGEZCOUNT = 0
    JEQMCOUNT = 0
    JEQZCOUNT = 0

    JLECOUNT = 0
    JLTCOUNT = 0

    JALCOUNT = 0
    JRCOUNT = 0

    def __init__(self, **kwargs):
        super().__init__(token = HlToken(), **kwargs)

    def next_value(self, line):
        line, a = self.next_token()
        if self.token.is_number(a):
            return parse_int(a)
        elif self.token.is_symbol(a):
            return a
        else:
            Error("argument in pseudo instruction must be symbol or number, {} given in line {}".format(a, line))

    def emit_label(self, label, line):
        self.parse_label(line, label + ":")

    def emit_seek(self, addr, line):
        self.parse_seek(line, "@" + hex(addr))

    def emit_subleq(self, a, b, c, line):
        self.program.set(a, line)
        self.program.set(b, line)
        self.program.set(c, line)

    def emit_sub(self, a, b, line):
        self.emit_subleq(b, a, Subleq.NEXT, line)

    def emit_movneg(self, a, b, line):
        self.emit_sub(a, a, line)
        self.emit_sub(a, b, line)

    def emit_mov(self, a, b, line):
        self.emit_movneg(self.TEMPS[0], b, line)
        self.emit_movneg(a, self.TEMPS[0], line)

    def emit_add(self, a, b, line):
        self.emit_movneg(self.TEMPS[0], b, line)
        self.emit_sub(a, self.TEMPS[0], line)

    def emit_clear(self, a, line):
        self.emit_sub(a, a, line)

    def emit_ldi(self, a, b, line):
        self.LDICOUNT += 1
        pre = "_LDI{}_".format(self.LDICOUNT)
        addr = pre + "ADDR"

        self.emit_mov(addr, b, line)

        self.emit_clear(self.TEMPS[0], line)

        self.emit_label(addr, line)
        self.emit_sub(self.TEMPS[0], 0xffff, line)
        self.emit_movneg(a, self.TEMPS[0], line)

    def emit_sti(self, a, b, line):
        self.STICOUNT += 1
        pre = "_STI{}_".format(self.STICOUNT)
        addr0 = pre + "ADDR0"
        addr1 = pre + "ADDR1"
        addr2 = pre + "ADDR2"

        self.emit_mov(addr0, b, line)
        self.emit_mov(addr1, b, line)
        self.emit_mov(addr2, b, line)

        self.emit_movneg(self.TEMPS[0], a, line)

        self.emit_label(addr0, line)
        self.program.set(0xffff, line)
        self.emit_label(addr1, line)
        self.program.set(0xffff, line)
        self.program.set(Subleq.NEXT, line)

        self.program.set(self.TEMPS[0], line)
        self.emit_label(addr2, line)
        self.program.set(0xffff, line)
        self.program.set(Subleq.NEXT, line)

    def emit_jmp(self, a, line):
        self.emit_subleq(self.TEMPS[0], self.TEMPS[0], a, line)

    def emit_jlez(self, a, b, line):
        self.emit_subleq(self.ZERO, a, b, line)

    def emit_jgez(self, a, b, line):
        self.JGEZCOUNT += 1
        pre = "_JGEZ{}_".format(self.JGEZCOUNT)
        after = pre + "AFTER"

        self.emit_jeqm(a, after, line)
        self.emit_movneg(self.TEMPS[0], a, line)
        self.emit_jlez(self.TEMPS[0], b, line)
        self.emit_label(after, line)

    def emit_jeqm(self, a, b, line):
        self.JEQMCOUNT += 1
        pre = "_JEQM{}_".format(self.JEQMCOUNT)
        after = pre + "AFTER"
        lez = pre + "LEZ"

        self.emit_jlez(a, lez, line)
        self.emit_jmp(after, line)

        self.emit_label(lez, line)
        self.emit_mov(self.TEMPS[1], a, line)
        self.emit_sub(self.TEMPS[1], self.ONE, line)
        self.emit_jlez(self.TEMPS[1], after, line)
        self.emit_jmp(b, line)

        self.emit_label(after, line)

    def emit_jeqz(self, a, b, line):
        self.JEQZCOUNT += 1
        pre = "_JEQZ{}_".format(self.JEQZCOUNT)
        after = pre + "AFTER"
        lez = pre + "LEZ"

        self.emit_jlez(a, lez, line)
        self.emit_jmp(after, line)

        self.emit_label(lez, line)
        self.emit_jgez(a, b, line)
        self.emit_label(after, line)

    def emit_jle(self, a, b, c, line):
        self.JLECOUNT += 1
        pre = "_JLE{}_".format(self.JLECOUNT)
        safe = pre + "SAFE"
        gez_a = pre + "GEZ_A"
        after = pre + "AFTER"

        self.emit_jgez(a, gez_a, line)
        self.emit_jgez(b, c, line)

        self.emit_label(safe, line)
        self.emit_mov(self.TEMPS[1], a, line)
        self.emit_sub(self.TEMPS[1], b, line)
        self.emit_jlez(self.TEMPS[1], c, line)
        self.emit_jmp(after, line)

        self.emit_label(gez_a, line)
        self.emit_jgez(b, safe, line)

        self.emit_label(after, line)

    def emit_jge(self, a, b, c, line):
        self.emit_jle(b, a, c, line)

    def emit_jlt(self, a, b, c, line):
        self.JLTCOUNT += 1
        pre = "_JLT{}_".format(self.JLTCOUNT)
        after = pre + "AFTER"

        self.emit_jeq(a, b, after, line)
        self.emit_jle(a, b, c, line)

        self.emit_label(after, line)

    def emit_jgt(self, a, b, c, line):
        self.emit_jlt(b, a, c, line)

    def emit_jeq(self, a, b, c, line):
        self.emit_mov(self.TEMPS[2], a, line)
        self.emit_sub(self.TEMPS[2], b, line)
        self.emit_jeqz(self.TEMPS[2], c, line)

    def emit_jal(self, a, b, line):
        self.JALCOUNT += 1
        pre = "_JAL{}_".format(self.JALCOUNT)
        addr = pre + "ADDR"
        after = pre + "AFTER"
        self.emit_mov(a, addr, line)
        self.emit_jmp(b, line)
        self.emit_label(addr, line)
        self.program.set(after, line)
        self.emit_label(after, line)

    def emit_jr(self, a, line):
        self.JRCOUNT += 1
        pre = "_JR{}_".format(self.JRCOUNT)
        addr = pre + "ADDR"
        self.emit_mov(addr, a, line)

        self.program.set(self.TEMPS[0], line)
        self.program.set(self.TEMPS[0], line)
        self.emit_label(addr, line)
        self.program.set(0xffff, line)

    def emit_hlt(self, line):
        self.emit_subleq(self.HALTADDR, self.HALTADDR, self.HALTADDR, line)

    def parse_ops(self, line, count, handler):
        ops = []
        for i in range(count):
            ops.append(self.next_value(line))
        handler(*ops, line)

    def parse_token(self, line, token):
        if token == "SUBLEQ":
            self.parse_ops(line, 3, self.emit_subleq)
        elif token == "SUB":
            self.parse_ops(line, 2, self.emit_sub)
        elif token == "MOVNEG":
            self.parse_ops(line, 2, self.emit_movneg)
        elif token == "MOV":
            self.parse_ops(line, 2, self.emit_mov)
        elif token == "ADD":
            self.parse_ops(line, 2, self.emit_add)
        elif token == "CLEAR":
            self.parse_ops(line, 1, self.emit_clear)
        elif token == "LDI":
            self.parse_ops(line, 2, self.emit_ldi)
        elif token == "STI":
            self.parse_ops(line, 2, self.emit_sti)
        elif token == "JMP":
            self.parse_ops(line, 1, self.emit_jmp)
        elif token == "JLEZ":
            self.parse_ops(line, 2, self.emit_jlez)
        elif token == "JGEZ":
            self.parse_ops(line, 2, self.emit_jgez)
        elif token == "JEQM":
            self.parse_ops(line, 2, self.emit_jeqm)
        elif token == "JEQZ":
            self.parse_ops(line, 2, self.emit_jeqz)
        elif token == "JLE":
            self.parse_ops(line, 3, self.emit_jle)
        elif token == "JGE":
            self.parse_ops(line, 3, self.emit_jge)
        elif token == "JLT":
            self.parse_ops(line, 3, self.emit_jlt)
        elif token == "JGT":
            self.parse_ops(line, 3, self.emit_jgt)
        elif token == "JEQ":
            self.parse_ops(line, 3, self.emit_jeq)
        elif token == "JAL":
            self.parse_ops(line, 2, self.emit_jal)
        elif token == "JR":
            self.parse_ops(line, 1, self.emit_jr)
        elif token == "HLT":
            self.parse_ops(line, 0, self.emit_hlt)
        else:
            super().parse_token(line, token)

class DebugHlAssembler(HlAssembler, DebugAssembler):
    def emit_subleq(self, a, b, c, line):
        self.program.reset_count()
        super().emit_subleq(a, b, c, line)
