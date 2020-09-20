# Writeup

Challenge starts with a webpage which reference a down game. Inspecting the source we see a reference to https://epicgame.play.duc.tf navigating to this website gives us the error `DNS_PROBE_FINISHED_NXDOMAIN`. This means the DNS server could not find an IP for this address. Let's see if we can find anything else.

Looking for TXT records with

`dig epicgame.play.duc.tf TXT` we get back a TXT file with the flag 