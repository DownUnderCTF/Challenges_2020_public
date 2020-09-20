# Writeup

You are given three bits of information: an item to find, along with a given location and date.

- item: a "big American refuelling plane"
- location: "boxing croc"
- date/time: September 1st 2020

Search engine search of "refuelling plane" reveals that they are typically military aircraft.

Search engine search of "boxing croc", reveals it is located at 326 Arnhem Hwy, Humpty Doo NT 0836.

You can assume that September 1st refers to 2020.

Search for "how to track military aircraft online" gives this link https://gijn.org/planespotting-a-guide-to-tracking-aircraft-around-the-world/
Which lists the first site for tracking military flights suggested is: ADS-B.NL

Have to also remember to limit by sites that give historical data, and not just real time tracking.

On http://ads-b.nl/ can limit for flights over the Australia region in the last month 
http://ads-b.nl/index.php?pageno=303&selectmove=month and then scroll down to locate 2020-09-01

Only 5 flights from America are listed as having flown this day. 
4 are K35R -> Tanker Jets.

Manually checking them reveals two flights that flew over Humpty Doo, and only one flew closely over the Boxing Croc http://www.ads-b.nl/track.php?AircraftID=11404929&datum=20200901&selectmove=month

The Registration for this plane is listed as: 58-0086

Search engine search with "58-0086" gives https://planefinder.net/data/aircraft/58-0086 which includes information such as the aircrafts, age, and first flight: 16-07-59.

Flag: DUCTF{16-07-59}