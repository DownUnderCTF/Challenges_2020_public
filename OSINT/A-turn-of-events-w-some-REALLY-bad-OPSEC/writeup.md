# Writeup

> **A turn of events w/ some REALLY bad OPSEC**
>
>We have identified the key suspect in multiple crimes, with authorities in pursuit. The suspect has been placed on the Interpol red list, and is believed to have already escaped the country through some unknown form of transport. Locating the transport the suspect took will be vital, and with lives on the line, time is of the essence. Provided attached is the evidence collected in this case.
>
> When you have determined which transport the suspect took, please submit it to us in the form of a flag containing the transports call sign and name, all uppercase, with any spaces replaced by underscores.
Flag format: DUCTF{callsign_name}
>
> **Category:** OSINT
>
> **Difficulty level:** Hard
>
> **Author:** scsc
>
> **Files**
> - ./challenge/suspect-file_AU00045733.jpg (sha265: 8ad129ebd167d4edb504a55e4551e73b1ed1e9209c8eba89a415a2c6eb72b859)

## Solution

*Unfortunately we made a mistake when creating this challenge, and as a result it had to be re-released at 01:45 2020-09-19, this impacted a bit of the flow of the challenge and it was still solvable but not as clean as the original*

With this challenge you need to identify the transport some suspect has taken to escape the country in the format DUCTF{callsign_name}, and are given a file "suspect-file_AU00045733.jpg" containing useful information to do so. Unfortunately, some of the data is missing from the file, as it was corrupted during transmission, so you will have to fill in the gaps using your own research.

The notable information to be gathered from the file is as follows:
- Identifying information for the suspect:
	- o█session██ith█gelato
	- Own████Ca█ name██Ale█andros
- Location information:
	- Last lo██tion:
		- wifi█████ MAC Ad███ss: `f8:ab:05:cf:37:54`
- Date/time information:
	- SUSPE███PL██S TO █EAV███AT ███ 2020-09-18
     - *[In the original version of the challenge this date was 2020-09-06]*
- Suspect activities:
	- seen frequently texting on what ██pears to be a burner phone
	- Active on social media

The first data point that stands out is "Own████Ca█ name██Ale█andros", and "o█session██ith█gelato" , as this indicates that the suspect in question is in fact Emily Waters from the previous Welcome to Petstagram challenge, who owned a cat named Alexandros, and seemed to have a love for gelato.

With this we have access to her social media as collected for the previous challenge:

> Twitter: https://twitter.com/gelato_elgato
>
> Instagram: https://www.instagram.com/emwaters92/ ,  https://www.instagram.com/alexandrosthecat/
>
> Youtube: https://www.youtube.com/channel/UCyPtfFTdCoLk7jSE7P1qsOg
>
> Email: emilytwaters92@gmail.com

Unfortunately the section of the subject file referring to her last known location is largely corrupted, however it does contain a MAC Address: `f8:ab:05:cf:37:54`. Using https://wigle.net/ you can locate the MAC Address (and Emily's last known location) as belonging to a wireless access point at Titanic Theatre Restaurant at 1 Nelson Pl, Williamstown VIC 3016.

The next piece of data "SUSPE███PL██S TO █EAV███AT ███ 2020-09-18" appears to state that the subject plans to leave at some time on the 18th of September, 2020, though the time is obscured.

The next step is to examine Emily's social media "Active on social media", starting with her Twitter Account.
A search of Emily's twitter account locates a post made at 1:03 AM, Sep 7, 2020, stating that she had "lots of fun plans this week!!" (https://twitter.com/gelato_elgato/status/1302623446979866624), and more notably, from 1:21 AM, Sep 7, 2020 made a series of posts surrounding concerns brought up by this video: https://www.youtube.com/watch?v=3m5qxZm_JqM&feature=youtu.be, https://twitter.com/gelato_elgato/status/1302628077810278403. The video features a skit referring to an incident wherein the "front fell off" a tanker ship, and Emily appears to show deep concern that this is a regular occurrence, indicating perhaps that she could be taking a ship in the near future. No further data can be obtained from Emily's twitter account, so the next step is to examine her Instagram.

Emily's Instagram contains two posts, a picture of her cat, and a video seemingly taken within some kind of cafe: https://www.instagram.com/p/CEzKUbeAMG-/, posted at 2020-09-06T15:02:38.000Z (Mon, 7 Sep 2020 01:02:38 +10:00). The description of the video is: "coffee and gelato earlier today with this cutie 😘😚☕🍨. sorry for the annoying background noise lol so annoying!!!!! 😤😡". From the description could be assumed that this video was taken at some point during the day on 6th September 2020.

The location of this video is tagged as "Gelateria on the Docks", a gelateria in Melbourne's docklands at G07 Star Cres, Docklands VIC 3008. This is the second reference to locations near the Port of Melbourne in Emily's post, and the third relating to ships.

The background noise she refers to could be a loud beeping noise very audible in the background of the video.
In conjunction with the hint "seen frequently texting on what ██pears to be a burner phone" you can determine that this is actually DTMF signalling, sounds made by a phone keypad.
To convert these sound to key presses, you can either record the sound with a DTMF app, or on your computer and upload to a site such as: http://dialabc.com/sound/detect/ which should give you a string of numbers: 6338063028090300.

The agent noted that Emily had been texting on her burner phone frequently, so you can assume that these key presses are from sending a text message. This could be through multi-tap, or t9 texting, however due to the formation of the keys (barely any repeating numbers), it would make sense to try t9 first. https://www.dcode.fr/t9-cipher.

```
63380	MEET > "MEET "
630	MD, ME, MF, ND, NE, NF, OD, OE, OF > "ME "
280	AT, AU, AV, BT, BU, BV, CT, CU, CV > "AT "
90	W, X, Y, Z > ?
30	D, E, F > ?
00   > ?
```

The decoder as given in the example picks up the first three words well "meet me at", separated by 0's however, it is not capable of identifying numbers, and is somewhat confused by the last characters "09 03 00". 9 and 3 could be letters, as shown above, or alternatively this could be a time: 930 > 9:30. For now you can assume it is a time.

The total information you now have is:
Emily's recent locations all centre around the Port of Melbourne.
She has indicated a present fear of the front of a tanker ship falling off.
Emily texted someone on September 6th that she would "meet [them] at 930".
According to the agent Emily planned to leave/begin transport at 2020-09-18.

The next step is to locate a boat that left from Port of Melbourne after 9:30 on 18th September 2020.
Using a site like https://www.myshiptracking.com/ you can check all marine traffic during a time period at a specific port. Traffic in the Port of Melbourne between 2020-09-18 00:00 ~ 2020-09-18 23:59 can be found at:
https://www.myshiptracking.com/ports-arrivals-departures/?mmsi=&pid=293&type=0&time=1600351200_1600437540&pp=20

> *This is the point where the challenge deviates from the original version, the original ship that Emily would have taken arrived in port at exactly 21:30 on the day noted by the agent (which was originally the 6th).*
>
> *However, in the final version of the challenge, now set on the 18th, it was instead that there was only one Tanker leaving* ***after*** *9:30. This added an unfortunate extra level of guessiness to the challenge. If you had previously noted her "tanker" video on twitter and identified the tanker as being of significance then it would not make as much of a difference, as only one tanker left port after 9:30 on the 18th.*

A few boats leave Port Melbourne on the 18th, however only one is a tanker that leaves after 9:30am,
https://www.myshiptracking.com/vessels/cap-victor-mmsi-240584000-imo-9321720
Clicking through to its page will give you the tankers call sign: SWHR, allowing you to complete your flag.


- Callsign: SWHR
- Name: CAP VICTOR

Flag: `DUCTF{SWHR_CAP_VICTOR}`
