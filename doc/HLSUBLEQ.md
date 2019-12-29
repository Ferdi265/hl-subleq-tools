# HLSUBLEQ instruction set and assembler

This page describes the instruction set, and the assembler syntax, operation,
and invocation of the `subleq-hlasm` and `subleq-hlsim` programs.

## Assembler Invocation

```
subleq-hlasm <file.hlsbl> <out> [dryrun] [debug] [lsim]
```

The general behaviour and invocation of the assembler is the same as
`subleq-asm`, see [ASSEMBLER.md](ASSEMBLER.md).

### Options

Note: The `debug` option will print the resulting SUBLEQ code _after applying
any expansions of HLSUBLEQ instructions_, which makes this option a useful
debugging tool for the HLSUBLEQ assembler (hence the name).

## Simulator Invocation

```
subleq-hlsim <file.hlsbl> [n]
```

The general behaviour and invocation of the simulator is the same as
`subleq-sim`, see [SIMULATOR.md](SIMULATOR.md).

## Instruction Set

The HLSUBLEQ instruction set is a set of mnemonics that expand to sequences of
SUBLEQ instructions.

- instructions implemented using self-modifying code are marked with (\*)
- those using any of the three temporaries `_TEMP0`, `_TEMP1`, and `_TEMP2` are
  marked with (T0), (T1), or (T2)
- those using the constants `_ZERO` or `_ONE` are marked with (Z) or (O)
- those using the halt address label `_HALT` are marked with (H)
- those creating new labels in the program are marked with (L)

### Instruction Set Listing

- `SUBLEQ a, b, c`: a plain SUBLEQ instruction, but using a mnemonic
- `SUB a, b`: subtract `b` from `a`, storing the result in `a`
- `CLEAR a`: set `a` to zero by subtracting it from itself
- `MOVNEG a, b`: move the negation of `b` into `a`
- `MOV a, b` (T0): move the value of `b` into `a`
- `ADD a, b` (T0): add the value of `b` to `a`
- `JMP a` (T0): unconditionally branch to `a`
- `LDI a, b` (\*T0L): move the value at the address in `b` to `a`
- `STI a, b` (\*T0L): move the value in `a` to the address in `b`
- `JLEZ a, b`: branch to `b` if `a` is less than or equal to zero
- `JGEZ a, b` (T0T1L): branch to `b` if `a` is greater than or equal to zero
- `JEQM a, b` (T1L): branch to `b` if `a` is equal to the most negative 16-bit
  two's complement number, -0x8000
- `JEQZ a, b` (T0T1L): branch to `b` if `a` is equal to zero.
- `JLE a, b, c` (T0T1L): branch to `c` if `a` is less than or equal to `b`
- `JGE a, b, c` (T0T1L): branch to `c` if `a` is greater than or equal to `b`
- `JLT a, b, c` (T0T1T2L): branch to `c` if `a` is less than `b`
- `JGT a, b, c` (T0T1T2L): branch to `c` if `a` is greater than `b`
- `JEQ a, b, c` (T0T1T2L): branch to `c` if `a` is equal to `b`
- `JAL a, b` (\*L): unconditionally branch to `b` and store the address of the
  instruction that would otherwise be executed next in `a`
- `JR a` (\*T0L): unconditionally branch to the address in `a`
- `HLT` (H): halts the machine

## Assembler Operation

The HLSUBLEQ assembler operates mostly the same way as `subleq-asm`
(see [ASSEMBLER.md](ASSEMBLER.md)), with the addition that there are now a
few special mnemonics that expand to sequences of SUBLEQ instructions
implementing a specific operation.

These new mnemonics have a higher priority than other assembler features, so a
label with the same name as a HLSUBLEQ instruction will never override the
instruction.

## Required Labels

Every HLSUBLEQ program is required to define the following labels for use by the
implementation when instructions are used that use them (see Instruction Set
Listing):

- `_ZERO`: the integer constant 0 (currently unused)
- `_ONE`: the integer constant 1 (currently unused)
- `_TEMP0`, `_TEMP1`, `_TEMP2`: temporary storage locations for use by the
  implementation.
- `_HALT`: the address accessed when the `HLT` instruction is used.

## Examples

Examples can be found in the [examples/hlsbl](../examples/hlsbl) directory.
