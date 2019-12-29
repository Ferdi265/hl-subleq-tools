# SUBLEQ simulator

This page describes the operation and invocation of the `subleq-sim`
assembler-level simulator program.

## Simulator Invocation

```
subleq-sim <file.sbl> [n]
```

The simulator will read the file `file.sbl`, assemble it (see
[doc/ASSEMBLER.md](ASSEMBLER.md)), and simulate up to `n` instructions
(or until the machine halts if `n` is not given).

## Simulator Operation

The simulator internally derives from the Assembler, and will assemble the
program given before simulation. A future version of the simulator may be able
to load assembled hex files or [Logisim](http://www.cburch.com/logisim/) memory
image files using an option flag.

The simulator will read in a full SUBLEQ instruction (3 16-bit words), execute
it, and move on to the next instruction. When the HALT address is part of the
instruction (0xffff), or when the maximum number of instructions is reached,
the simulator terminates.

A future version of the simulator may be able to print a debug trace using the
`debug` option. The functionality is implemented (see `DebugSimAssembler` in
`hlsubleq.sim`), but not exposed through the CLI as of now.

## Examples

Examples can be found in the [examples/sbl](../examples/sbl) directory.
