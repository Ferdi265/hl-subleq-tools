def create_assembler(ifaces):
    class Asm(*ifaces):
        pass

    return Asm
