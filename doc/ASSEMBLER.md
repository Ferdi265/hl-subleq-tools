# SUBLEQ assembler

This page describes the syntax, operation and invocation of the `subleq-asm`
assembler program.

## Assembler Invocation

```
subleq-asm <file.sbl> <out> [dryrun] [debug] [lsim]
```

The assembler will read the file `file.sbl`, assemble it, and write the output
to the file `out`.

### Options

- `dryrun`: don't actually write any files
- `debug`: print out every `number`, `symbol`, `label` definition, or `seek`
  when encountering them, creating a pretty-printed version of the program. Not
  very useful for `subleq-asm`, but more useful for `subleq-hlasm` (see
  [doc/HLSUBLEQ.md](HLSUBLEQ.md))
- `lsim`: by default, the assembler prints the assembled program in hex, one
  16-bit word per line. This option enables [Logisim](http://www.cburch.com/logisim/)
  memory image format instead.

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

### Special Symbols

The special symbols `NEXT` and `AGAIN` can be used to refer to the address of
the beginning of the _next_ instruction or the start of the _current_
instruction (effectively executing the instruction _again_), respectively, when
used in the branch slot of a SUBLEQ instruction.

The special symbol `NONE` can be used to define consecutive storage locations at
the end of the memory image without having them be zero-filled in the memory
image file.

## Examples

Examples can be found in the [examples/sbl](../examples/sbl) directory.
