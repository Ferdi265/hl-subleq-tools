# SUBLEQ assembler

This page describes the syntax, operation and invocation of the `subleq-asm`
assembler program.

## Assembler Invocation

TODO

## Assembler Operation

The assembler syntax used by the `subleq-asm` assembler is very rudimentary,
and due to there being only a single instruction, has no concept of an
instruction mnemonic.

### Tokens

These are the different kinds of tokens the assembler supports, separated by
whitespace (an 'int' in this context is a hexadecimal (preceded by `0x`) or
decimal signed number), in parse priority order:

- `seek`: an `@` symbol, followed by an 'int'
- `label`: a string of non-whitespace characters, followed by a `:` symbol
- `number`: a hexadecimal (preceded by `0x`) or decimal signed integer
- `symbol`: a string of non-whitespace characters

### Operation

Every token the assembler reads that is not a `seek` or `label` token will be
translated into a single word in the resulting memory image. 

- `number` tokens will be literally placed in the memory image
- `symbol` tokens will be expanded to the memory offset where the corresponding
  `label` definition was encountered in a second pass.

The `seek` token will set the current memory offset to the given value, leaving
the memory in between undefined. Undefined memory will be set to zero in the
second assembler pass.

## Examples

Examples can be found in the [examples/sbl](../examples/sbl) directory.
