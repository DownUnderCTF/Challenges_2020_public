# Tim Tams
We are provided with Clive.wav, an audio file that sounds kinda like a fax tone.

Upon some googling, we discover that its actually SlowscanTV: https://www.wikpedia.org/Slow-scan_television.

Slow Scan television (SSTV) is a picture transmission method used mainly by amateur radio operators, to transmit and receive static pictures via radio in monochrome or color.

We learnt that: 

There are a number of different modes of transmission, but the most common ones are Martin M1 (popular in Europe) and Scottie S1 (used mostly in the USA).

We should probably try M1 and S1 as they are some of the most commonly used types.

I used Black Cat SSTV (https://www.blackcatsystems.com/software/sstv.html) as my decoder --> works on both Windows/Mac but the following guide should help if you were wanting to decode using a Linux OS:

https://ourcodeworld.com/articles/read/956/how-to-convert-decode-a-slow-scan-television-transmissions-sstv-audio-file-to-images-using-qsstv-in-ubuntu-18-04

Depends on the software used but you'll have to play with the Skew & Offset values to be able to view the image cleanly.

You'll end up with an image of Clive Palmer and the following text in the top left corner: QHPGS{UHZOYR_Z3Z3_1BEQ}

Decode that as Rot13 using CyberChef and you'll recieve the flag:

DUCTF{HUMBLE_M3M3_1ORD}