from .asm import *
from .asmext import *

class SimAssembler(ArrayOutputAssembler):
    def get_addr(self, addr):
        if addr < len(self.out_memory):
            return self.out_memory[addr]
        else:
            return 0

    def set_addr(self, addr, word):
        while addr >= len(self.out_memory):
            self.out_memory.append(0)
        self.out_memory[addr] = word

    def fetch_instruction(self, pc):
        return self.get_addr(pc), self.get_addr(pc + 1), self.get_addr(pc + 2)

    def execute_instruction(self, ap, bp):
        a, b = self.get_addr(ap), self.get_addr(bp)
        b = twos2neg(b) - twos2neg(a)
        self.set_addr(bp, neg2twos(b))
        return b

    def branch(self, pc, b, c):
        if b <= 0:
            return c
        else:
            return pc + 3

    def simulate(self, n = None):
        i = 0
        pc = 0
        while n == None or i < n:
            ap, bp, c = self.fetch_instruction(pc)
            if ap == 0xffff or bp == 0xffff or c == 0xffff:
                return

            b = self.execute_instruction(ap, bp)
            pc = self.branch(pc, b, c)

            i += 1

class DebugSimAssembler(SimAssembler):
    def fetch_instruction(self, pc):
        ap, bp, c = super().fetch_instruction(pc)
        a, b = self.get_addr(ap), self.get_addr(bp)
        print("[DBG] {:04x} {:04x} {:04x}".format(ap, bp, c))
        print("..... {:04x} {:04x}".format(a, b))
        return ap, bp, c


    def branch(self, pc, b, c):
        newpc = super().branch(pc, b, c)
        if pc + 3 == c:
            pass
        elif newpc == pc + 3:
            print("..... {:04x} >  0, don't branch".format(b))
        else:
            print("..... {:04x} <= 0, branch to {:04x}".format(b, c))
        return newpc
