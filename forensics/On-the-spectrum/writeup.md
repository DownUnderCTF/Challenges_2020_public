# Writeup

> **On the spectrum**
>
> My friend has been sending me lots of WAV files, I think he is trying to communicate with me, what is the message he sent?

You are given a file "message_1.wav", it won't be much more than random audio noises if you play it, but this audio represents something - data.

The challenge name gives the first hint "On the spectrum" , which indicates that audio can be viewed in a spectrum format.

The description further asks to work out the message that is being sent by their friend.

From the following information, a search for any of the included terms like "spectrum", "wav", "audio files" will bring up spectogram, spectrum analyzer or audacity itself.

Next, you will want to view the audio file in a sepctrogram using a application that has a spectrum analyzer. A common free tool to do this is Audacity (https://www.audacityteam.org/)

From here, if the file is opened in audacity, by default the file will show the waveform. By clicking on the name for the track, you can switch the view to spectogram. 

Lastly, zooming in on the spectogram you are able to see the flag inscribed in the spectogram.

Flag: DUCTF{m4by3_n0t_s0_h1dd3n}
