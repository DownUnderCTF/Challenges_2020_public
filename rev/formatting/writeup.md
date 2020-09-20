# formatting

this is an easy "stack strings" challenge. `sprintf` is used to piece a flag together.

solvable with both static and dynamic analysis techniques, but the easiest way is to use `ltrace` and/or `gdb` to set a breakpoint after sprintf and look at the output.

