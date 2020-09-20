homepage
=========

thought that this would be a fun challenge for people starting out! on second thoughts,
it mightve been highly annoying and not "beginner"

the flag will be hidden in the logo, top to bottom, then left to right. this is hinted by
the colour gradient. when planning the challenge it should be able to be done manually,
but there are 405 dots and getting one wrong will probably get you the wrong result. therefore 
an automated method might be a bit better.

on inspection, there is some javascript code inside /scripts/splash.js with a variable called lol
containing the binary. however, just trying to decode this binary string will produce gibberish
as the binary code is encrypted with the position of the circle elements in the SVG (i guess you
could say it's a one time pad).

therefore to solve this programatically, you would need to unshuffle the SVG circles as well as
the `lol` code. once that is done, the binary can just be read as an ASCII string.

a solve script is provided detailing what is happening.
