# hl-subleq-tools

This repository contains a set of tools for writing programs in the
[SUBLEQ](https://en.wikipedia.org/wiki/One_instruction_set_computer#Subtract_and_branch_if_less_than_or_equal_to_zero)
machine, as well as a software simulator.

## SUBLEQ

The SUBLEQ instruction is a combined arithmetic and conditional jump
instruction:

```
subleq a, b, c
```

also sometimes written

```
subleq [a], [b], c
```

It is equivalent to the following C-like pseudo code:

```c
*b -= *a;
if (*b <= 0) pc = c;
```

This single instruction is sufficient to implement arbitrary programs.

### Implementation

The assembler and simulator in this repository implement a 16-bit variant of
SUBLEQ using Two's Complement arithmetic with word-addressed memory.

Each memory word is 16 bits, each SUBLEQ instruction is 3 consecutive possibly
unaligned memory words. Execution starts at address `0x0000`.

Any fetch from address `0xffff` halts the machine. This includes operand fetches
/ deref.

## Tools

The tools provided in this package are the following:

- `subleq-asm`: a simple assembler for SUBLEQ, syntax and behaviour further
  described in [doc/ASSEMBLER.md](doc/ASSEMBLER.md)
- `subleq-sim`: an assembler-level simulator for SUBLEQ, behaviour further
  described in [doc/SIMULATOR.md](doc/SIMULATOR.md)
- `subleq-hlasm`: a 'higher level' macro assembler that expands instruction
  mnemonics down to SUBLEQ, instruction set further described in
  [doc/HLSUBLEQ.md](doc/HLSUBLEQ.md)
- `subleq-hlsim`: an extension of the `subleq-sim` simulator to HLSUBLEQ,
  further described in [doc/HLSUBLEQ.md](doc/HLSUBLEQ.md)
